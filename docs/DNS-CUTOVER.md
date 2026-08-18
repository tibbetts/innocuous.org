# DNS cutover: Gandi → Cloudflare, innocuous.org → bulrushlabs.com

Working runbook. Captured state is from 18 August 2026, before any change.
`bulrushlabs.com` becomes canonical and serves the Hugo site from GitHub Pages;
`innocuous.org` becomes a path-preserving 301 in front of it.

## Pre-flight, verified 18 Aug 2026

- **DNSSEC is OFF on all four domains** (no DS at the registry). A nameserver
  change is therefore safe. If DNSSEC is ever turned on, it must be disabled and
  the DS record allowed to expire *before* changing nameservers, or resolution
  breaks hard for everyone with a validating resolver.
- Registrar for all four is Gandi. `innocuous.org` already uses Cloudflare DNS;
  the other three use Gandi DNS.
- Cloudflare account is `Tibbetts@gmail.com's Account`
  (`e2e601b16d453e5e4e6f4b65efdbbe12`), already holding `innocuous.org` and
  `probcomp.org`.

## Live things that must not break

**`innocuous.org` is not just a website.** The zone carries mail and subdomains:

| Record | Value | Status | Action |
|---|---|---|---|
| `innocuous.org` MX | Fastmail (`in1`/`in2-smtp.messagingengine.com`) | **live mail** | preserve exactly |
| `tna.innocuous.org` MX | Fastmail, MX only, no A | **structural, confirmed by RT** | preserve exactly — never match with a wildcard |
| `innocuous.org` A | `65.19.178.79`, proxied | dead origin — this is the 522 | replaced by redirect |
| `www` CNAME | `uist.aletta.net`, proxied | dead | replaced by redirect |
| ~~`mull` A~~ | `45.33.75.56` (Linode) | dead | **pruned 18 Aug 2026** |
| ~~`play` A~~ | `66.228.35.54` (Linode) | dead | **pruned 18 Aug 2026** |
| `new` CNAME | `uist.aletta.net` | dead | left in place — not yet reviewed |

The redirect rule must be scoped to **apex + www only**, never `*.innocuous.org`,
or it will swallow `tna` and the mail subdomain stops resolving as expected.

## Captured Gandi zones (the three being moved)

Everything below is Gandi's default template except where marked. The
`webredir`/`blogs`/`smtp`/`imap`/`webmail` names all point at Gandi-hosted
services and **stop working the moment DNS leaves Gandi** — do not recreate them.

**bulrushlabs.com** — the only zone with real content:

| Type | Name | Value | Keep? |
|---|---|---|---|
| MX | @ | `1 aspmx.l.google.com`, `5 alt1`, `5 alt2`, `10 aspmx2`, `10 aspmx3` | yes, verbatim |
| TXT | @ | `v=spf1 include:_spf.google.com ~all` | yes, verbatim |
| TXT | @ | `google-site-verification=jFQy3Djbz4l9xA49RoVldeEviLZZfnnukMr3hP8vV_M` | yes, verbatim |
| A | @ | `217.70.184.38` (Gandi parking) | no — replaced by Pages |
| CNAME | www | `webredir.vip.gandi.net` | no — dies with Gandi |
| — | smtp, imap, webmail, blog | Gandi services | no — die with Gandi |

**bulrushlabs.org** and **bullrushlabs.com** — pure Gandi boilerplate, nothing
worth carrying over. Both become redirect-only zones.

Mail note: the Google records are preserved **even though mail is moving to
Fastmail**. A provider migration should be a no-op; change one variable at a
time, so tomorrow's breakage can't be the mail. Do Fastmail as its own deliberate
change once the zone is stable. Keeping the `google-site-verification` TXT also
preserves the ability to prove ownership when releasing the domain from the
Google Workspace tenant, which is the step people get stuck on.

## Phase 1 — zones into Cloudflare (no user-visible change)

1. Create Cloudflare zones for `bulrushlabs.com`, `bulrushlabs.org`,
   `bullrushlabs.com` on the account above.
2. Populate from the tables above. Do **not** import the Gandi service names.
3. For each redirect-only hostname, add a dummy proxied record so Redirect Rules
   have something to fire against (see Phase 3):
   `A @ 192.0.2.1 proxied` and `A www 192.0.2.1 proxied`.
4. Change nameservers at Gandi to the pair Cloudflare assigns per zone.
5. Wait for each zone to report `status=active`.

Verify before moving on:

```bash
for d in bulrushlabs.com bulrushlabs.org bullrushlabs.com; do
  echo "== $d"; dig +short NS $d; dig +short MX $d
done
```

## Phase 2 — bulrushlabs.com serves the site

6. In the `bulrushlabs.com` zone, replace the parking A record with GitHub Pages:
   `A @ 185.199.108.153`, `.109.153`, `.110.153`, `.111.153` — **DNS-only (grey
   cloud)**, and `CNAME www tibbetts.github.io`, also DNS-only. Grey matters:
   Pages needs an unproxied view of the host to provision its Let's Encrypt
   certificate. It can be switched to proxied afterwards.
7. Commit `static/CNAME` containing `bulrushlabs.com`, push, then set the custom
   domain in the repo's Pages settings. Wait for the certificate, then enable
   Enforce HTTPS.

Verify — and do not proceed until this passes:

```bash
curl -sI https://bulrushlabs.com | head -1
curl -sI https://bulrushlabs.com/articles/2015/05/01/startups-intellectual-property-boston-inn-of-courts/ | head -1
```

## Phase 3 — redirects (ONLY after Phase 2 verifies)

**Do not enable this before bulrushlabs.com actually serves the site.** Enabling
it early 301s twenty years of inbound links to a parking page, and search engines
follow 301s and reindex. The current 522 is treated as transient; a 301 to the
wrong place is not.

8. `innocuous.org` Redirect Rule — apex and www only:

```
when:  (http.host eq "innocuous.org") or (http.host eq "www.innocuous.org")
then:  dynamic → concat("https://bulrushlabs.com", http.request.uri.path)
       status 301, preserve query string
```

Leave `tna` and `new` untouched; the rule matches on exact host, so they are
unaffected. (`mull` and `play` were pruned 18 Aug 2026.)

9. Same rule shape on `bulrushlabs.org` and `bullrushlabs.com`, both → 301 to
   `https://bulrushlabs.com` with path preserved.

Verify:

```bash
curl -sI http://innocuous.org/articles/2015/05/01/startups-intellectual-property-boston-inn-of-courts/ | head -3
dig +short MX innocuous.org        # must still be Fastmail
dig +short MX tna.innocuous.org    # must still be Fastmail
```

## Phase 4 — registrar transfers

10. After Gandi's 72-hour hold releases the auth codes, transfer to Cloudflare
    Registrar. Each transfer **adds a year** to the existing expiry, so nothing
    already paid for is lost.
11. **`bullrushlabs.com` first — it expires 2026-09-27.** Its whois Updated Date
    is 2026-08-18, which may indicate a 60-day registrant-change lock that would
    outlast that expiry. Check its transfer eligibility in Gandi before relying
    on the transfer; if it is locked, renew it at Gandi for a year and transfer
    later. Do not attempt to thread a transfer through an expiry date.

## Later, deliberately separate

- Move `bulrushlabs.com` mail to Fastmail; drop the Google MX/SPF once mailboxes
  exist and the Workspace tenant has released the domain.
- Consider octoDNS to keep these zones as code in this repo, so a future provider
  move is a config change and records cannot be silently lost.
