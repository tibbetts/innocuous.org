# Monitoring

Synthetic checks for the site and its domains. **Not uptime monitoring** — a
generic uptime service watches the one thing least likely to break here.

## What this catches that an uptime checker does not

The failure modes created by the 18 August 2026 DNS cutover are all silent:

| Failure | Why uptime monitoring misses it |
|---|---|
| The `innocuous.org` → `bulrushlabs.com` 301 stops preserving paths | The site still returns 200. Every 2005–2015 permalink lands on the homepage and nothing looks wrong. |
| A Fastmail MX record vanishes | No HTTP check can see MX records. You find out when someone says they emailed weeks ago. |
| A second SPF record appears | Multiple SPF records are a permanent error under RFC 7208 — mail auth breaks for *every* sender at once. This nearly happened during the Fastmail move. |
| A domain expires | `bullrushlabs.com` expires 2026-09-27. |
| The TLS certificate fails to renew | GitHub auto-renews, but not infallibly. |

## Usage

```bash
./tools/monitoring/site-check.py       # silent on success; failures to stdout; exit 1
./tools/monitoring/site-check.py -v    # print every check
./tools/monitoring/site-check.py --no-whois   # skip registry expiry
```

Runs in ~3s. No credentials needed — `curl`, `dig`, `whois`, and Python's `ssl`.
Registry expiry is cached for 12h in `~/.cache/bulrush-site-check/` because
`whois` is slow and rate-limited.

## Wiring

`watch.sh` drives it from a persistent Monitor, emitting **only on state
change** — once when checks start failing, once when they recover. A naive
`|| echo` reprints the same failure every cycle for an entire outage, which
trains you to ignore it.

```
Monitor: cd /path/to/repo && INTERVAL=900 ./tools/monitoring/watch.sh
         persistent: true
```

Monitors are session-scoped and do not survive a restart. For monitoring that
outlives a session, this needs an external scheduler (launchd on the Mac, or a
GitHub Actions scheduled workflow).

## Two deliberate design choices

**DNS queries go to the authoritative nameserver** (`@earl.ns.cloudflare.com`),
never the local resolver. During the cutover, a stale cache returned a **200
from the old Gandi parking page** — a false pass indistinguishable from
success. Checks that can be fooled by cache are worse than no checks.

**HTTP checks pin the origin IP** with `curl --resolve` for the same reason.

## Known non-failure

DKIM currently reports a note, not a failure: the CNAMEs resolve to Fastmail
correctly but publish `p=` with no key material
(`Intentionally_Left_Blank_As_Per_DKIM_Rotation_BCP`). That is Fastmail's
placeholder until signing is enabled for the domain in their UI. The DNS side
is complete; the signing side is not.
