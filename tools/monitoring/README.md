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

## The self-test

The first check is a **live negative control**, borrowed from `reading-leveler`
after their post-deploy checker passed on a build that had the bug it existed
to catch. Their detector asserted "status is not 404"; the historical broken
deployment sat behind Vercel auth and answered `401`, which satisfied it. Two
failures compounding: a detector too loose to mean anything, and a fixture that
could no longer express the failure.

Their generalisation is the useful part: **a negative test needs a fixture that
can actually express the failure**, and the most durable source of one is
something that is *supposed* to fail that way, permanently, by design. A
historical broken build drifts — it gets wrapped in auth, redeployed, deleted.
A by-design behaviour does not.

Here that fixture is `http://innocuous.org/`. It really does 301 to
`https://bulrushlabs.com/` — correct behaviour, and therefore a permanent live
example of a redirect target that does *not* equal the deep path. It runs
through the same comparison the real detector uses and must be rejected. If it
is ever accepted, the comparison has gone lenient (substring, prefix,
trailing-slash normalisation) and **every redirect PASS above it is worthless**.

The self-test is itself negative-tested: it fires both when the control stops
redirecting and when the control unexpectedly matches.

## Two bugs found by reading someone else's notebook

`rubicon-ux` wrote up a branch that had been "verified in the dark": its tests
ran in a git worktree, where the gitignored `.env.local` does not exist, so
every run took a credential-absent fallback — and the tests asserted that
fallback as the expected result. Green in the worktree and green on `main`
meant different things, and nothing anywhere said so.

Reading that surfaced the same shape here, twice:

**1. A partial whois cache produced a full pass.** `check_domain_expiry`
iterated the *cache* rather than `DOMAINS`, so a cache covering one domain
checked one domain and reported `registry expiry ok`. Not hypothetical — this
repo's own negative test wrote exactly such a one-domain cache. Had it not been
cleaned up, the check would have watched one domain of four for twelve hours
while reporting green, and `bullrushlabs.com` (expires 2026-09-27) is one of
the three it would have stopped watching. Now the cache is used only if it
covers every domain, and the loop iterates `DOMAINS` so an absent result is a
reported failure.

**2. An unverifiable expiry whispered instead of failing.** A domain whose
whois could not be parsed appended a *note*, and notes only print in verbose
mode or alongside other failures — so under the Monitor it was silent. "I could
not determine the expiry" rendered identically to "the expiry is fine." Now it
fails.

Both are the same rule, which is worth stating once: **a check that cannot run
must never be indistinguishable from a check that ran and passed.**

## Known non-failure

DKIM currently reports a note, not a failure: the CNAMEs resolve to Fastmail
correctly but publish `p=` with no key material
(`Intentionally_Left_Blank_As_Per_DKIM_Rotation_BCP`). That is Fastmail's
placeholder until signing is enabled for the domain in their UI. The DNS side
is complete; the signing side is not.
