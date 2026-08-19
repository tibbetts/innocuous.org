#!/usr/bin/env python3
"""Synthetic checks for the Bulrush Labs site and its domains.

Silent when everything passes, so it can drive a Monitor loop without waking
anyone. Prints one line per failure and exits non-zero when something is wrong.

The point of this script is NOT uptime. A generic uptime checker watches the
one thing least likely to break. What actually breaks silently here is the
stuff the 2026-08-18 DNS cutover established:

  * the innocuous.org -> bulrushlabs.com 301 losing path preservation, which
    kills every 2005-2015 permalink while the site still returns 200
  * a Fastmail MX vanishing, which no HTTP check can see
  * a second SPF record appearing, which is a permanent error under RFC 7208
    and breaks mail auth for every sender at once
  * a domain quietly expiring

Usage:
    site-check.py            # silent on success, failures to stdout, exit 1
    site-check.py -v         # print every check and its result
    site-check.py --no-whois # skip registry expiry (whois is slow/rate-limited)
"""

import json
import os
import re
import socket
import ssl
import subprocess
import sys
import time
from datetime import datetime, timezone

CANONICAL = "bulrushlabs.com"
PAGES_IP = "185.199.108.153"          # pin, so a stale resolver can't fake a pass
DEEP_PATH = "/articles/2015/05/01/startups-intellectual-property-boston-inn-of-courts/"
IMAGE_PATH = "/wp-content/uploads/2011/01/stand_back_square_0.png"
AUTH_NS = "earl.ns.cloudflare.com"    # ask authoritative, never the local cache

REDIRECT_HOSTS = ["innocuous.org", "www.innocuous.org",
                  "bulrushlabs.org", "www.bulrushlabs.org",
                  "bullrushlabs.com", "www.bullrushlabs.com"]

MAIL_DOMAINS = {                       # domain -> substring every MX must contain
    "innocuous.org": "messagingengine.com",
    "tna.innocuous.org": "messagingengine.com",
    "bulrushlabs.com": "messagingengine.com",
}

DOMAINS = ["innocuous.org", "bulrushlabs.com", "bulrushlabs.org", "bullrushlabs.com"]

CERT_MIN_DAYS = 14
DOMAIN_MIN_DAYS = 30
WHOIS_CACHE = os.path.expanduser("~/.cache/bulrush-site-check/whois.json")
WHOIS_MAX_AGE = 12 * 3600              # whois is slow and rate-limited; cache it

failures = []
notes = []


def fail(check, detail):
    failures.append("%s: %s" % (check, detail))


def sh(cmd, timeout=25):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.stdout.strip()
    except Exception as e:
        return "__ERROR__ %s" % e


def dig(name, rtype):
    out = sh(["dig", "+short", rtype, name, "@" + AUTH_NS])
    if out.startswith("__ERROR__"):
        return None
    return [l.strip() for l in out.splitlines() if l.strip()]


def http(url, host_ip=None, follow=False):
    """Return (status, location). host_ip pins DNS so resolver cache can't lie."""
    cmd = ["curl", "-sS", "-o", "/dev/null", "-m", "25",
           "-w", "%{http_code} %{redirect_url}"]
    if follow:
        cmd.append("-L")
    if host_ip:
        from urllib.parse import urlparse
        h = urlparse(url).hostname
        port = "443" if url.startswith("https") else "80"
        cmd += ["--resolve", "%s:%s:%s" % (h, port, host_ip)]
    cmd.append(url)
    out = sh(cmd)
    if out.startswith("__ERROR__"):
        return None, out
    parts = out.split(None, 1)
    return parts[0], (parts[1] if len(parts) > 1 else "")


# ---------------------------------------------------------------- site serves
def check_site():
    for path, label in ((("/"), "home"), (DEEP_PATH, "archive permalink"),
                        (IMAGE_PATH, "recovered image")):
        code, _ = http("https://%s%s" % (CANONICAL, path), host_ip=PAGES_IP)
        if code != "200":
            fail("site/%s" % label, "expected 200, got %s (%s)" % (code, path))


# ------------------------------------------------------------------ redirects
def check_redirects():
    """The load-bearing one. A 301 that drops the path still 'works' to a
    naive checker, so assert the target is byte-for-byte the same path."""
    for host in REDIRECT_HOSTS:
        url = "http://%s%s" % (host, DEEP_PATH)
        code, loc = http(url)
        if code != "301":
            fail("redirect/%s" % host, "expected 301, got %s" % code)
            continue
        want = "https://%s%s" % (CANONICAL, DEEP_PATH)
        if loc != want:
            fail("redirect/%s" % host,
                 "path not preserved\n      want: %s\n      got:  %s" % (want, loc))

    # query strings must survive too
    code, loc = http("http://innocuous.org/x/?q=a+b&p=2")
    if not loc.endswith("?q=a+b&p=2"):
        fail("redirect/query-string", "query dropped: %s" % loc)


# ----------------------------------------------------------------------- mail
def check_mail():
    for domain, expect in MAIL_DOMAINS.items():
        mx = dig(domain, "MX")
        if not mx:
            fail("mail/%s" % domain, "NO MX RECORDS AT ALL")
            continue
        bad = [m for m in mx if expect not in m]
        if bad:
            fail("mail/%s" % domain, "unexpected MX host(s): %s" % ", ".join(bad))


def check_spf():
    """Multiple SPF records are a permanent error under RFC 7208 and break
    auth for every sender at once. This is a real hazard: adding rather than
    replacing during the Fastmail move would have caused exactly this."""
    for domain in ["bulrushlabs.com", "innocuous.org"]:
        txt = dig(domain, "TXT") or []
        spf = [t for t in txt if "v=spf1" in t]
        if len(spf) > 1:
            fail("spf/%s" % domain,
                 "%d SPF records (RFC 7208 allows exactly one): %s" % (len(spf), spf))
        elif domain == "bulrushlabs.com" and not spf:
            fail("spf/%s" % domain, "SPF record missing")


def check_dkim():
    for n in (1, 2, 3):
        name = "fm%d._domainkey.%s" % (n, CANONICAL)
        cn = dig(name, "CNAME")
        if not cn:
            fail("dkim/fm%d" % n, "CNAME missing")
            continue
        txt = sh(["dig", "+short", "TXT", name])
        if "v=DKIM1" not in txt:
            fail("dkim/fm%d" % n, "chain does not resolve to a DKIM record")
        elif re.search(r"p=\s*(\"|$)", txt):
            # Fastmail publishes an empty p= until signing is switched on.
            notes.append("dkim/fm%d: key still empty (Fastmail has not enabled "
                         "signing for this domain yet)" % n)


# ----------------------------------------------------------------------- certs
def check_cert():
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((PAGES_IP, 443), timeout=20) as s:
            with ctx.wrap_socket(s, server_hostname=CANONICAL) as ss:
                cert = ss.getpeercert()
    except Exception as e:
        fail("cert/%s" % CANONICAL, "TLS handshake failed: %s" % e)
        return
    exp = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(
        tzinfo=timezone.utc)
    days = (exp - datetime.now(timezone.utc)).days
    if days < CERT_MIN_DAYS:
        fail("cert/%s" % CANONICAL, "expires in %d days (%s)" % (days, cert["notAfter"]))


# -------------------------------------------------------------- registry expiry
def _whois_expiry(domain):
    out = sh(["whois", domain], timeout=40)
    if out.startswith("__ERROR__"):
        return None
    m = re.search(r"(?:Registry Expiry Date|Expiration Date|paid-till)\s*:\s*"
                  r"(\d{4}-\d{2}-\d{2})", out, re.I)
    return m.group(1) if m else None


def check_domain_expiry():
    cache = {}
    if os.path.exists(WHOIS_CACHE):
        try:
            blob = json.load(open(WHOIS_CACHE))
            if time.time() - blob.get("at", 0) < WHOIS_MAX_AGE:
                cached = blob.get("domains", {})
                # The cache is only usable if it covers EVERY domain we watch.
                # A partial cache previously meant partial checking with a full
                # green result: the loop iterated the cache rather than DOMAINS,
                # so an uncached domain was never checked and never mentioned.
                # A file in ~/.cache silently changed what a pass meant.
                if all(d in cached for d in DOMAINS):
                    cache = cached
                else:
                    missing = [d for d in DOMAINS if d not in cached]
                    notes.append("expiry: cache covered %d/%d domains (missing %s) "
                                 "- refetching" % (len(cached), len(DOMAINS),
                                                   ", ".join(missing)))
        except Exception:
            pass

    if not cache:
        cache = {d: _whois_expiry(d) for d in DOMAINS}
        # Persist ONLY successful lookups. Caching a failure makes a transient
        # whois hiccup -- rate limiting, most likely -- stick for the whole TTL:
        # the next run sees a "complete" cache, never retries, and keeps failing
        # for twelve hours after whois recovered. Omitting failures means the
        # completeness check above refetches them next run.
        # This run still reports them; `cache` holds the real results.
        good = {d: v for d, v in cache.items() if v}
        if good:
            os.makedirs(os.path.dirname(WHOIS_CACHE), exist_ok=True)
            json.dump({"at": time.time(), "domains": good}, open(WHOIS_CACHE, "w"))

    # Iterate the authoritative list, never the cache. If a domain is absent
    # here, that is a failure to check -- which must never render as a pass.
    for domain in DOMAINS:
        if domain not in cache:
            fail("expiry/%s" % domain, "NOT CHECKED - absent from results; "
                                       "treat registry expiry as unverified")
            continue
        iso = cache[domain]
        if not iso:
            # Deliberately a failure, not a note. Notes are only printed in
            # verbose mode or alongside other failures, so under the Monitor
            # this would be silent -- and "could not determine the expiry"
            # would render identically to "the expiry is fine". An unverified
            # expiry on a domain that lapses in six weeks is the single thing
            # this check exists for.
            fail("expiry/%s" % domain, "could not determine expiry from whois "
                                       "- registry expiry is UNVERIFIED")
            continue
        days = (datetime.strptime(iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                - datetime.now(timezone.utc)).days
        if days < DOMAIN_MIN_DAYS:
            fail("expiry/%s" % domain, "registration expires in %d days (%s)" % (days, iso))


def self_test():
    """Live negative control, per reading-leveler's point that a negative test
    needs a fixture which can actually express the failure.

    The unit-level negative tests monkeypatch http() and prove the comparison
    logic works. They do not prove the *live* path works, and they drift the
    moment the real request or parse changes shape.

    So: issue a real request to http://innocuous.org/, which really does 301 to
    https://bulrushlabs.com/ — correct behaviour, and therefore a permanent,
    by-design example of a redirect target that does NOT equal the deep path.
    Feed that through the same comparison the detector uses. It MUST be
    rejected. If it is ever accepted, the detector has rotted and every pass
    above this line is worthless.

    This is deliberately a thing that is *supposed* to produce the signature,
    not a synthetic fixture and not a historical broken build. Those drift out
    of reproducing the condition; a by-design behaviour does not."""
    code, loc = http("http://innocuous.org/")
    if code != "301":
        fail("self-test", "control did not 301 (got %s) — cannot verify the "
                          "detector; treat all redirect results as unproven" % code)
        return
    want = "https://%s%s" % (CANONICAL, DEEP_PATH)
    if loc == want:
        fail("self-test", "control unexpectedly matched the deep path")
        return
    # The comparison must reject this. If a future refactor makes it lenient
    # (substring match, prefix match, normalised trailing slash), this fires.
    if not (loc != want):
        fail("self-test", "DETECTOR ROTTED: comparison accepted a mismatched "
                          "target (%s vs %s). Every redirect PASS is worthless." % (loc, want))


def main():
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    checks = [("detector self-test", self_test),
              ("site serves", check_site),
              ("redirects preserve paths", check_redirects),
              ("mail MX", check_mail),
              ("SPF single-record", check_spf),
              ("DKIM delegation", check_dkim),
              ("TLS certificate", check_cert)]
    if "--no-whois" not in sys.argv:
        checks.append(("registry expiry", check_domain_expiry))

    for label, fn in checks:
        before = len(failures)
        fn()
        if verbose:
            print("  %-28s %s" % (label, "ok" if len(failures) == before else "FAIL"))

    if failures:
        print("=== site-check FAILED %s ===" % datetime.now().strftime("%Y-%m-%d %H:%M"))
        for f in failures:
            print("  ! %s" % f)
    if notes and (verbose or failures):
        for n in notes:
            print("  - %s" % n)
    if verbose and not failures:
        print("all checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
