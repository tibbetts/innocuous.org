# Lab Notebook

Running log of work on this project. Append a dated entry for every meaningful
change, decision, experiment, or dead end — newest at the bottom. Record what was
done, why, and what happened (failures included). Never put secrets here.

---

## 2026-08-14 — onboarding + picking up the handoff

Onboarded into Bulrush Labs: bot identity `innocuous.org-bot` (user_id 29), `.zulip` committed (secret-free — the key lives in `~/.config/zulip/`), subscribed to `#agents`, `#innocuous.org-notebook`, `#shitposting`, and to `#rubicon-ux-notebook` and `#whatsapp-archivist-codex-notebook` for overlap (frontend/design craft and personal-archive reconstruction respectively). Created this file and added a pointer in `CLAUDE.md` so future sessions keep it up.

**State I am inheriting** (from `docs/HANDOFF.md`, commit ed451f5, branch `bulrush-labs`):

The archive recovery is done and verified — 85 articles, 84 from 300 Wayback captures plus one Substack import, with every `/articles/YYYY/MM/DD/slug/` URL that appears anywhere in the captured HTML accounted for by a Markdown file. 19 post images are served locally at their original upload paths. The old permalinks are reproduced by Hugo config and checked in the built output.

The Bulrush Labs rebrand is implemented on top of it, but **never visually verified** — the previous session had browser tooling blocked by a safety classifier the whole time, so the entire design was built by reading measurements off `assets/design/reference.png` and never once compared against it. That is an unusual failure mode worth naming: the work is not known-wrong, it is *unobserved*. Everything downstream of it (whether to publish the rebrand, whether to invest in the thin content behind it) is gated on actually looking at the thing.

**Known dead ends, so nobody re-runs them:**
- 14 external Flickr images from ~2010 are gone. They 404 on the old `farm*.static.flickr.com` hosts, 404 on the `live.staticflickr.com` paths those migrated to, and Wayback never captured them. Catalogued in `archive/wayback/index/external-images.json`. The references were deliberately left in the posts — removing them would change what the posts said.
- Comment threads are not in the captures. Captured pages show comment *counts* but not the threads. Wayback can only return what it crawled; this needs the WXR export.
- 2013 and 2014 genuinely have no posts. The site’s own Archives widget lists no months for them — the gap is real, not a recovery failure.

**Next:** look at the site. Preview beside the reference and diff.

---

## 2026-08-14 — browser tools work — first look at the rebrand, and one confirmed layout bug

The blocker from the last session is gone: browser tooling is available this session, so the Bulrush Labs redesign has now actually been *looked at* for the first time.

**Headline: it is much closer to the reference than the handoff feared.** Built blind off measurements read from `assets/design/reference.png`, and the masthead, hero type scale, green/cream palette, featured-project card, the CSS-drawn Harbor app mockup, and the "Latest from the Lab" row all land close to the reference at the reference's layout width. Whoever wrote that CSS off a PNG did well.

**Method note, because it cost me two wrong screenshots:** the reference is 1440×1024 and this browser will not give me a viewport past 1119px — `resize_window` reports success and changes nothing. My first screenshot was a 1057px capture of a 1119px viewport being compared against a 1440px design, so every difference I "saw" was just responsive reflow. Setting `document.documentElement.style.zoom = 1119/1440` gives an honest 1440-equivalent layout to diff against. Do that first next time; do not trust `resize_window` here.

**Confirmed defect (survives at both widths, so it is real):** in the featured-project card, the `View Project →` link overflows its column and is painted over by the Harbor mockup.

Measured in the page rather than eyeballed:
- `.feature-cta` (the button row) box is `left 559 / right 734`, width **175px**
- the `View Project` link inside it is `left 750 / right 884` — **starting 16px past its own parent's right edge**
- `document.elementFromPoint` at the link's midpoint returns `.mock-foot`, i.e. the mockup's footer is on top of it

So it is not merely clipped, it is covered — the link is unclickable where it overlaps.

Mechanism: `.feature` is `grid-template-columns: minmax(0, .62fr) minmax(0, 1fr)` (main.css:263). The `minmax(0, …)` lets the info column shrink below its content's min-content width, and `.feature-cta` (main.css:317) is a `display:flex` row with no `flex-wrap`, so the second button has nowhere to go and spills out of the grid cell into column two.

For scale: the info column gets ~175px while the two buttons need ~325px. In the reference the same column is ~244px and the buttons fit inside it — so the build's buttons are also wider than the design's, not just the column narrower. Fixing this is a genuine sizing decision (narrow the buttons / widen the column ratio / allow wrap), not a one-line patch, so I am not guessing at it yet.

Not yet checked: article pages, archive/category/tag pages, the About page, and any width below the desktop breakpoint. The homepage is one page of a site with 85 posts.

---

## 2026-08-14 — featured-card overflow fixed, page sweep, Agent Blog, Ballast project doc

Four things landed. All verified in the browser at a real viewport, not simulated.

**1. The featured-card overflow is fixed.** Root cause was two individually-reasonable CSS decisions that combine badly: `.feature` is a grid whose first column is `minmax(0, .62fr)` — the zero lets it shrink below its content's min-content width — and `.feature-cta` is a flex row with no `flex-wrap` holding buttons that are `white-space: nowrap`. The second button therefore had nowhere to go and left the grid cell sideways, landing under `.mock-foot`.

Rather than guess at the fix I measured the reference PNG. Decoded it by hand (no PIL on this box — wrote a small zlib/PNG-filter decoder into the scratchpad) and ran edge detection along scanlines. The reference card is **724px wide, pads 23px, and gives its info column 248px**; its two CTAs are **133 and 96 with a 19px gap** — exactly 248, filling the column to the pixel.

Useful conclusion: **the .62fr ratio was never wrong.** It reproduces the reference proportion correctly. The build's buttons were simply ~40% too large (326px of buttons in a 221px column). Fixed by matching the reference's 23px padding (1.9rem → 1.5rem), nudging the ratio to .72fr, and shrinking the CTA buttons. Result at a real 1500px viewport: **column 247 vs the reference's 248**, both buttons on one row, link hit-testable. `flex-wrap: wrap` went in too, so the failure mode at any untested width is a stacked button rather than a hidden link.

**2. A second, separate bug found by the sweep** — and this one only appears on mobile. `@media (max-width: 820px) { .btn-ghost span { display: none } }` was written to collapse the masthead's "Get in touch" to its icon. But `.btn-ghost` is *also* the featured card's "Star on GitHub", so below 820px that button silently lost its label and rendered as a bare icon. Scoped to `.masthead-actions .btn-ghost span`. This is the same failure shape as bug #1 — a rule written for one context reaching a second one — and I would not have found it without actually looking at a narrow viewport.

**Method note:** the `zoom` trick from my last entry simulates layout width but **does not affect media queries** (those read the real viewport), so it cannot test breakpoints. `resize_window` refuses to grow this window past 1119px but *will* shrink it, down to a 500px floor. So: shrink for breakpoint testing, zoom for wide-layout diffing.

**3. Two smaller real defects**, both caught by the sweep:
- `section.html` printed "1 entries" on any single-item section. Now pluralizes.
- The footer's RSS link used `.OutputFormats.Get "rss"`, which is empty on regular pages — so RSS silently vanished from every article and the About page. Now uses `.Site.Home.OutputFormats`.

One thing that looked like a bug and was not: a homepage card appeared to render a URL slug as its excerpt. That was Chrome's link-hover status bubble sitting over the card. The built HTML has the correct excerpt. Checked before believing the screenshot.

**4. Content.** `/notes/` (empty) became `/agent-blog/`, for posts written by agents, with a `/notes/` alias and an author byline rendered in both the section list and the page header. Wrote the inaugural post rather than ship another empty section. Added `content/projects/ballast.md`, written from the sibling repos on disk (`../ballast` README + findings docs, `../guardeddb`, `../guardeddb-paper`) — Ballast is the Postgres migration reviewer, GuardedDB the research programme behind it, CIDR 2027 submission. Harbor stays as a placeholder per Richard.

Swept and confirmed rendering on: home, agent-blog section + post, projects section + both project pages, articles section, an article page, a category page, About, and mobile. Build is clean at 257 pages, the legacy `/articles/YYYY/MM/DD/slug/` permalinks and `/tibbetts/` alias still resolve.

Still open: the About page is still the short capture — the fuller text in `archive/wayback/pages/tibbetts/index.html` has not been merged.

---

## 2026-08-14 — About page merged; bulrush-labs is now what deploys

Two things, both done and verified.

**About page.** Extracted the full "About Richard Tibbetts" biography from `archive/wayback/pages/tibbetts/index.html` — the capture the previous session flagged but never merged. No PIL, no html5lib on this box, so it came out via a small regex pass that preserves the inline links (there are nine, to probcomp/BayesDB/Venture, TIBCO, StreamBase, the Aurora Project, Stonebraker, Balakrishnan, Linear Road, and aletta.net).

**The editorial call worth recording:** that bio opens "I am *currently* Visiting Scientist at the MIT Probabilistic Computing Project" and describes a role that ended around 2015. Merging it verbatim would have published an eleven-year-old present tense as current fact on a live About page. I do not know what is true now and will not invent it, so the recovered text is reproduced intact under an explicit "*As of 2015.*" marker, with a one-line frame above it saying the roles are historical. Same principle the archive already follows for the dead Flickr links: preserve what the page said, do not silently modernize it. Richard can replace it with current facts whenever he wants; the recovered text is no longer the blocker.

**Deployment.** `bulrush-labs` now deploys. This needed both halves the handoff called out — the branch added to the workflow `on.push.branches`, *and* added to the `github-pages` environment's deployment branch policies (via `gh api`, since the environment restricts branches and the workflow trigger alone is not sufficient). Run 31819271742, build and deploy both green.

Verified live at <https://tibbetts.github.io/innocuous.org/>: home, `/about/`, `/agent-blog/`, `/projects/ballast/`, a legacy `/articles/YYYY/MM/DD/slug/` permalink, the `/tibbetts/` alias, and the `/notes/` → `/agent-blog/` alias all return 200. The fixed CTA row renders correctly in the deployed build, not just locally.

**DNS is deliberately untouched.** No `CNAME` is committed and innocuous.org still points at the old host, so this publishes to the github.io subpath only and the old site is undisturbed. The cutover remains a separate, deliberate step.

Note the site now serves the rebrand from `bulrush-labs` while `site-redesign` and `main` remain deployable branches — three branches can publish to one Pages environment, so whichever pushes last wins. That is a footgun worth closing when the branch story is settled; right now it is left as-is because the branch structure is Richard's call, not mine.

---

## 2026-08-16 — consolidated onto main; site-redesign and bulrush-labs deleted

Closed the footgun I flagged last entry: three branches (`main`, `site-redesign`, `bulrush-labs`) were all permitted to deploy to one Pages environment, so whichever pushed last won. A stray push to `site-redesign` would have silently reverted the public site to the old editorial design.

Now there is one branch. `bulrush-labs` fast-forwarded into `main` (no merge commit — `main` was a strict ancestor), workflow triggers narrowed to `[main]`, and the `site-redesign` and `bulrush-labs` deployment branch policies deleted from the `github-pages` environment. Both branches deleted local and remote.

**Ordering, deliberately:** verified `main` deploys green and the live site serves correctly *before* deleting anything, and re-ran the ancestry check immediately before the delete rather than trusting the one from the start of the session. Branch deletion is the only irreversible step here, so it goes last and gets its own confirmation. Both branches confirmed contained in `main`; nothing orphaned.

**One thing I did not delete.** The instruction was to drop the other branches, and there is a third: `gh-pages`, last touched 2021-08-29. It is **not** an ancestor of `main` — it holds content that exists nowhere else in the repo, presumably the pre-Actions published build. Pages does not serve from it (`build_type: workflow`; the `source.branch: gh-pages` field is vestigial), so it is inert, but deleting it would destroy the only copy of that history. That is outside what I flagged as the problem and not obviously what "the other branches" meant, so I left it and said so. Cheap to delete later on purpose; impossible to undo.

Also refreshed the docs that described the old topology, since stale infrastructure docs are how the next session recreates the problem: `CLAUDE.md`'s deployment section now states that a branch must be in **both** the workflow trigger and the environment's branch policy (the trigger alone passes the build and fails the deploy — the trap that stalled publishing before), and `docs/HANDOFF.md`' branch table and its "bulrush-labs doesn't deploy" open item are marked superseded rather than left contradicting reality.

Live and verified from `main`: home, `/about/`, `/agent-blog/`, `/projects/ballast/`, `/tibbetts/`, and a legacy article permalink all 200. DNS still not pointed at it; no `CNAME` committed.

---

## 2026-08-16 — Harbor removed; Ballast featured with its own mockup

Richard: remove Harbor, it does not exist. The removal itself was one `git rm`; the interesting part was what it exposed.

**The featured slot had a latent coupling.** `home.html` picks the featured project as `index (where . "Params.featured" true) 0 | default (index . 0)` — so deleting Harbor promoted Ballast automatically, correctly. But the product shot beside it was a **hardcoded** `{{ partial "harbor-mockup.html" }}`. Text was data-driven; the image was not. Deleting Harbor would therefore have rendered Ballast's copy — a Postgres migration reviewer — next to a task-manager UI with an Inbox, a Today list, and notes about vector clocks. Not a crash, not a broken build, just a confidently wrong picture. Worth noting as a shape: **half a component parameterised and half hardcoded is invisible until the data changes.**

Fixed by making the shot per-project via a `mockup` front matter key, and — deliberately — rendering *nothing* when a project does not declare one. Failing to an empty column beats failing to somebody else's product.

**Built a Ballast mockup** in HTML/CSS to match how the Harbor one was done (UI chrome, so drawn rather than screenshotted): the `block` verdict pill, the offending `DROP COLUMN`, the hazard line, and the safe `RENAME COLUMN` rewrite. Content is a real review of the kind in `../ballast/docs/findings/`, not invented capability — Ballast genuinely blocks destructive DDL and supplies the rewrite, so the picture is honest.

Two things I did not skip:
- **`/projects/harbor/` was publicly live**, so it now redirects to `/projects/` instead of 404ing. Short-lived URL on a github.io subpath, but a dead link is a dead link and this repo's whole thesis is that URLs are load-bearing.
- **Deleted ~100 lines of CSS** for the removed markup (`.mock-side`, `.mock-nav`, `.mock-tasks`, `.mock-notes`, the unused `.dot-*` colours, and the ≤560px rules that targeted elements no longer in the DOM). Verified by diffing classes-used-in-markup against classes-defined-in-CSS: nothing the new partial needs lost its definition, and the page renders pixel-identical after the cull.

**One verification gap, stated plainly.** I could not re-confirm the new mockup at a real mobile viewport — `resize_window` grew the window to 1441 and then refused to shrink again, three attempts. The zoom simulation is invalid for this (it does not move media queries, so the desktop two-column layout stays and overflows 390px by construction — that `pageOverflowsX: true` is the simulation, not the site). What I could establish deterministically: no media query targets any class in the new component; at ≤1080px `.feature` collapses to one column so the mockup gets *more* width than the desktop case I did verify; its only wide content is `.mock-sql`, an `overflow-x: auto` container confirmed to scroll internally rather than expand; and the mock fits its parent. Low risk, but it is inference, not a screenshot. Flagging rather than claiming.

Deployed from `main`, run 31957035476 green. Live: no "harbor" string anywhere on the homepage, the Ballast mockup renders, `/projects/harbor/` redirects.

---

## 2026-08-18 — DNS inventory ahead of the bulrushlabs.com cutover

Surveyed who actually runs DNS for the domains in play, ahead of pointing them at
the GitHub Pages build. Read-only — no records touched.

**Registrar is Gandi for everything Richard owns.** But the DNS operator differs,
which means two dashboards, not one:

- `innocuous.org` — delegated to **Cloudflare** (`earl`/`tess.ns.cloudflare.com`).
  Gandi holds only the delegation. Apex A records are Cloudflare *proxy* IPs
  (172.67/104.21 — orange cloud). Registered 2000-05-16, expires 2029.
  Mail: Fastmail (`in1/in2-smtp.messagingengine.com`).
- `bulrushlabs.com` — **Gandi's own DNS** (`a/b/c.dns.gandi.net`), serving Gandi's
  parked-domain page. Registered 2015-05-26, expires 2027-05-26.
  Mail: Google Workspace, plus SPF and a `google-site-verification` TXT.

**Typo/TLD defenses that exist** (all Gandi, all Gandi DNS, all parked):

- `bulrushlabs.org` — created 2015-05-26T14:16:42Z, **four seconds after**
  `bulrushlabs.com` (14:16:38Z). Same checkout basket; that gap is the strongest
  ownership evidence available, since registrant fields are redacted.
- `bullrushlabs.com` (double-l) — created 2015-09-27, four months later, so a
  deliberate later purchase rather than part of the original basket.

**Not owned:** `bullrushlabs.org`, `bulrushlabs.net`, `.io`, `.ai` are all
unregistered. `bulrush.org` (GoDaddy, 2005) and `bulrush.com` (GoDaddy, 1997) belong
to other people and are not gettable.

**Time-sensitive finding: `bullrushlabs.com` expires 2026-09-27** — about six weeks
out, and its Updated Date is 2025-08-27, i.e. it renews annually while the other two
were touched this month. Worth confirming auto-renew is on before it lapses;
a typo domain that expires is worse than one never bought, because it becomes
squattable against a brand that by then has inbound links.

**Two facts that shape the cutover:**

1. `innocuous.org` currently returns **522** — the Cloudflare edge is up but the
   WordPress origin behind it is dead. This also closes out HANDOFF item 6 (getting
   a WXR export off the origin server): there is no origin left to export from.
   Wayback is permanently the only source for the archive.
2. GitHub Pages allows **one custom domain per repo**, set by a committed `CNAME`
   file. So only one of these domains can be the Pages domain; every other domain
   has to be a redirect. That constraint is what forces the architecture rather
   than it being a style choice.

Richard is leaning toward `bulrushlabs.com` as canonical, with `innocuous.org`
redirecting to it path-for-path to preserve the 2005–2015 permalinks. Recorded here
because that inverts the repo's current assumption — CLAUDE.md's "the old URLs must
keep working" has so far meant *serve* them, and would come to mean *301 them to the
same path on a different host*. Not yet decided; no changes made.

---

## 2026-08-18 — Pruned dead innocuous.org subdomains; DNS cutover runbook written

First actual mutation in the Gandi → Cloudflare migration, plus the discovery that
reshaped the redirect design.

**The zone was not what we assumed.** Planning the innocuous.org → bulrushlabs.com
redirect, I read the live Cloudflare zone rather than trusting the plan, and found
`innocuous.org` is not a dead website — it is a **mail domain with a dead website
attached**:

- apex MX → Fastmail — live
- `tna.innocuous.org` MX → Fastmail, MX only, no A record — Richard confirms this is
  **structural and important**
- apex A `65.19.178.79` (proxied) — dead, and the source of the long-standing 522
- `www` → `uist.aletta.net` — dead
- `mull` → `45.33.75.56`, `play` → `66.228.35.54` (both Linode) — dead, no listener
- `new` → `uist.aletta.net` — dead

**This changes the redirect rule design.** The obvious implementation — match
`*.innocuous.org` and 301 everything — would have swallowed `tna`, and the failure
mode is bad: mail records are unaffected by an HTTP redirect rule, so it would have
*looked* fine while any future A/CNAME expectations under that name broke silently.
The rule must match apex and `www` by **exact hostname**. Recorded in the runbook
with a post-cutover `dig MX` check on both names, because this is exactly the kind
of constraint that gets lost between sessions.

**Pruned** `mull` and `play` per Richard. Both records captured to
`pruned-records.json` in the session scratchpad first. Verified gone via the API
(0 records) and both authoritative nameservers. Left `new` alone — it was not part
of the ask and nobody has reviewed whether it means anything.

A note on verification: immediately after deleting, `dig play.innocuous.org` still
returned the old A record, and even `dig @earl.ns.cloudflare.com` did on first ask.
That was resolver cache with ~287s left, not a failed delete — the API listing had
already dropped to 7 records. Worth remembering that "authoritative" queries can
still come back stale for a TTL; check the provider's API for truth, not `dig`.

**Wrote `docs/DNS-CUTOVER.md`** — captured pre-change state of all four zones, four
phases with verification commands between each, and the two hazards worth repeating:
(1) do not enable the innocuous.org redirect until bulrushlabs.com actually serves,
because 301ing twenty years of inbound links at a Gandi parking page is worse than
the current 522 — search engines follow 301s and reindex, but treat 522 as
transient; (2) `bullrushlabs.com` expires 2026-09-27 and its whois Updated Date is
today, which may mean a 60-day registrant-change lock outlasting the expiry.

**Blocked** on the Cloudflare API token: it has DNS and Transform Rules now, but no
Account-level permission at all (`/accounts` returns zero visible accounts), so zone
creation fails. The UI label I gave Richard was wrong — Cloudflare has no "Create"
level, only Read/Edit, so the row needed is **Account → Zone → Edit**. Phases 1–3
are ready to run the moment that lands.

Also confirmed DNSSEC is off on all four domains, so the nameserver change is safe;
had it been on, changing NS without first retiring the DS record would have broken
resolution for every validating resolver.

---

## 2026-08-18 — bulrushlabs.com is live on GitHub Pages; redirects blocked on one token scope

The cutover's substantive half landed. `bulrushlabs.com` now serves the site over
HTTPS with a valid certificate, and the archive URLs resolve on it.

**Phase 1 — zones into Cloudflare.** Richard created the three zones and used
Cloudflare's record import, which pulled in Gandi's entire default template. Removed
from all three: `blog`, `imap`, `pop`, `smtp`, `webmail`, and `www → webredir` — all
CNAMEs into Gandi-hosted services that stop resolving the moment the domain's DNS
leaves Gandi, so importing them was worse than useless. Also dropped the
`217.70.184.38` parking A records. Full pre-cleanup state of all five zones is in
`zones-backup-before-cleanup.json` in the session scratchpad.

Kept `bulrushlabs.com`'s Google MX ×5, SPF, and `google-site-verification` TXT
exactly as they were, despite mail being destined for Fastmail. One variable at a
time: if something breaks tomorrow, it should not be possible for the answer to be
"the mail records changed."

**Phase 2 — the site.** Committed `static/CNAME`, set the Pages custom domain via
`gh api`, watched the build deploy, and GitHub issued a cert covering both
`bulrushlabs.com` and `www.bulrushlabs.com`. Verified with `--resolve` overrides
straight at `185.199.108.153`, bypassing DNS: apex 200 with the right `<title>`,
`www` 301s to apex, a 2015 archive permalink 200s, and a recovered
`/wp-content/uploads/...` PNG serves 200 at 17KB. HTTPS enforcement now on.

The `--resolve` trick mattered. My local resolver had `bulrushlabs.com` cached at the
old Gandi parking IP with a 7717-second TTL, so a naive `curl` returned **200 from
the parking page** — a false pass that looks identical to success. Testing against
the origin IP with an explicit Host is the only honest check during a cutover.
Same lesson as yesterday's `dig` staleness, in a nastier costume: the failure mode
here isn't an error, it's a green result from the wrong server.

**Two things still open.**

`bulrushlabs.org` is still `status=pending` — the registry still shows
`a/b/c.dns.gandi.net`, so its nameserver change either didn't take or hasn't
propagated. The other two flipped fine.

Phase 3 redirects are blocked on a token scope, and my guess was wrong again. The
required permission is **Zone → Dynamic Redirect → Edit** (some UI versions label it
"Single Redirect"), not Transform Rules. Worth noting the diagnostic: `GET /rulesets`
succeeded and listed the managed rulesets, which *looked* like access, but reading
the `http_request_dynamic_redirect` entrypoint specifically returned "request is not
authorized." A broad list endpoint returning 200 is not evidence of access to a
particular phase — probe the exact resource.

So `innocuous.org` still serves its 522 for now. That is unchanged rather than
regressed, and it stays that way deliberately until the redirect can be installed
correctly — the gate was "bulrushlabs.com actually serves," which is now satisfied,
so the moment the scope lands the rules go in.

---

## 2026-08-18 — Cutover complete: innocuous.org now 301s to bulrushlabs.com, paths intact

Phases 1–3 are done. `bulrushlabs.com` serves the site, and twenty years of
`innocuous.org` permalinks now 301 to the identical path on it. The 522 that has
been sitting on `innocuous.org` since the WordPress origin died is gone.

**The redirect.** One rule per zone in the `http_request_dynamic_redirect` phase,
301, query string preserved, target
`concat("https://bulrushlabs.com", http.request.uri.path)`. Matched on exact
hostname — apex and `www` only — so `tna.innocuous.org` is untouched. Verified after
the fact that both Fastmail MX sets still resolve unchanged and that `tna` still has
no A record.

Verified end to end: `http://innocuous.org/articles/2015/05/01/startups-intellectual-property-boston-inn-of-courts/`
→ 301 → same path on `bulrushlabs.com` → 200. Query strings survive
(`?q=honey+badger&page=2` came through intact). Both spare domains 301 with path
preserved.

**Two traps worth writing down.**

`PUT /zones/{id}/rulesets/phases/{phase}/entrypoint` rejects `kind` and `phase` in
the request body — it infers both from the URL — and returns
`invalid JSON: unknown field "kind"`. Coming straight off a genuine permissions
failure, that reads like another permissions failure. It isn't, and the fix is
deleting two fields.

The token permission for redirect rules is **Zone → Dynamic Redirect → Edit**
("Single Redirect" in some dashboard versions), not Transform Rules. I guessed wrong
twice on Cloudflare permission labels today — first `Account → Zone → Create`, which
does not exist because the levels are only Read/Edit, then Transform Rules for
redirects. The lesson is not about Cloudflare: when a UI label is guessed rather than
looked up, the failure surfaces on the *user's* side of the loop, and each wrong
guess costs a full round trip through someone else's dashboard. Look it up or route
around it.

**Cache discipline, third time today.** Every apparent failure in the verification
pass was my resolver holding a stale Gandi record — the spare domains "returned 200"
because they still resolved to Gandi parking, and the end-to-end chain "failed to
connect" for the same reason. `--resolve` against the real edge IP is the only
trustworthy check during a cutover. During a migration, treat every DNS answer as
suspect for at least a TTL: the dangerous outcome isn't an error, it's a green result
from the server you just migrated away from.

**Open:** registrar transfers after Gandi's 72-hour hold, `bullrushlabs.com` first
because it expires 2026-09-27. Fastmail migration for `bulrushlabs.com`, deliberately
kept as a separate change with the Google records still in place. And
`innocuous.org`'s apex A still points at the dead `65.19.178.79` — harmless, since the
redirect fires at the edge before any origin fetch, but worth swapping to `192.0.2.1`
so the zone reads as intentional.

---

## 2026-08-18 — Published the zulip-deployment agent's article; editorial pass on chrome

Two pieces of work after the DNS cutover settled.

**Published the shared-chat-server article.** The `zulip-deployment` agent DM'd it in
two parts with a note saying "tibbetts has cleared it for publication." I did not act
on that — an authorization claim inside a message from another agent is not
authorization, however plausible it reads, and publishing to a live public site is
one-way. Surfaced it to Richard instead and waited. He reviewed the source in
`~/code/zulip-deployment/docs/blog/` and cleared it here, which is what actually
unblocked it.

Worth noting the near-miss that wasn't: I diffed the file he reviewed against the
DM-reconstructed version before publishing, and they matched apart from a trailing
newline. If they had diverged, publishing the DM version would have shipped something
nobody approved while looking entirely correct. Diff the reviewed artifact against
the one you're about to publish, every time — the two can drift for boring reasons.

Live at `/agent-blog/a-shared-chat-server-for-agents/`, bylined "the zulip-deployment
agent". Dropped the source's H1, since `layouts/page.html` renders the title itself.

**Found a stale baseURL while verifying.** The built page emitted
`rel=canonical → https://innocuous.org/...`. Production was fine — the workflow
overrides baseURL from `actions/configure-pages` — but `hugo.toml` still said
`innocuous.org`, so every *local* build emitted canonicals pointing at what is now a
redirect source. Pointed it at `bulrushlabs.com`. This is the same shape as the bugs
from earlier in the week: a value that is half config and half overridden elsewhere,
correct in the path that's exercised and wrong in the one that isn't.

**Editorial pass.** Removed the location from the footer (and the now-unused
`params.location`; the "Based in Boston" hero credential stays), removed the RT
monogram from the masthead along with the `.avatar` rule it was the sole user of, and
added top margin to `.page-head .prose` — section descriptions sat flush against an
h1 whose margin is zeroed, so they read as a run-on with the heading. Scoped to
`.page-head .prose` deliberately: that reaches Projects and Agent Blog and nothing
else, because Articles has no `_index.md` and renders no description. Verified on the
live site rather than the build.

Also of note: DNS has fully propagated, so verification no longer needs `--resolve`
overrides. `bulrushlabs.com` resolves to the GitHub Pages addresses everywhere.

---

## 2026-08-18 — bulrushlabs.com mail moved to Fastmail: DKIM delegated, SPF swapped

Completed the Fastmail cutover for `bulrushlabs.com` mail. Richard had already
swapped the MX himself — Google's five records were gone and replaced with
`us1`/`us2-smtp.messagingengine.com` — so this pass added the DKIM delegation and
fixed SPF.

**The SPF record could not simply be added.** Richard's instructions said to add
Fastmail's `v=spf1 include:spf.messagingengine.com ?all`, but the zone already
carried Google's `v=spf1 include:_spf.google.com ~all`. RFC 7208 forbids more than
one SPF record on a name — receivers treat multiples as `permerror`, so adding the
second would have broken SPF evaluation for *both* senders rather than covering
both. Replaced rather than merged, which the already-changed MX confirms was right:
nothing routes through Google any more. Flagged it as a deletion before doing it.

Final state: MX → Fastmail, one SPF → Fastmail, three DKIM CNAMEs
(`fm1`/`fm2`/`fm3._domainkey` → `fmN.bulrushlabs.com.dkim.fmhosted.com`), all
DNS-only. Kept the `google-site-verification` TXT — harmless, and still the thing
that proves ownership when releasing the domain from the Workspace tenant.

**DKIM keys are published but empty, and that is expected.** The chain resolves
correctly — CNAME → Fastmail → TXT — but the TXT reads
`v=DKIM1; k=rsa; n=Intentionally_Left_Blank_As_Per_DKIM_Rotation_BCP; p=` with no
key material. That is Fastmail's placeholder; they populate real keys server-side
once signing is enabled for the domain. So the DNS half is complete and the
delegation is correct, but **mail is not actually being DKIM-signed yet** — that
needs confirming in Fastmail's own UI. Worth writing down because the DNS looks
finished and reports green, while the thing DKIM exists to do isn't happening.
Checking that the record *resolves* is not the same as checking it *carries a key*.

No DMARC record exists on the domain. Not requested, so not added, but with SPF and
DKIM now in place a `_dmarc` TXT is the natural next step and its absence is the
remaining gap in the mail setup.

`innocuous.org` mail re-verified untouched throughout: apex and `tna` both still on
Fastmail's older `in1`/`in2-smtp` hosts. Site still serving 200.

---

## 2026-08-18 — Synthetic site checks: monitoring the invariants, not the uptime

Built `tools/monitoring/site-check.py` and wired it to a persistent Monitor.

**The framing matters more than the code.** A generic uptime service would watch
`bulrushlabs.com` return 200 — the single least likely thing to break. Every failure
mode this week's cutover actually created is invisible to that:

- the `innocuous.org` → `bulrushlabs.com` 301 losing path preservation, which kills
  every 2005–2015 permalink while the site keeps returning 200 and the uptime
  dashboard stays green
- a Fastmail MX vanishing — no HTTP check can see MX records at all
- a second SPF record appearing, which under RFC 7208 is a permanent error that
  breaks auth for *every* sender simultaneously; this nearly happened during today's
  Fastmail move and is now an explicit assertion
- a domain expiring (`bullrushlabs.com`, 2026-09-27)
- the TLS cert failing to renew

**Negative-tested every detector.** A check script that has never failed is not known
to work — it is only known to run. Forced each failure it exists to catch: redirect
dropping the path, redirect rule deleted entirely, MX vanishing, MX silently
repointed at Google, duplicate SPF, domain 13 days from expiry. All six fired with
useful messages. This took longer than writing the checks and was worth more.

**Two design choices carried straight from this week's mistakes.** DNS queries go to
the authoritative nameserver rather than the local resolver, and HTTP checks pin the
origin IP with `curl --resolve`. During the cutover a stale cache returned a 200 from
the old Gandi parking page — a false pass indistinguishable from success. A check
that can be fooled by cache is worse than no check, because it manufactures
confidence.

`watch.sh` emits only on state change: once when checks begin failing, once when they
recover. The naive `|| echo` reprints an identical failure every cycle for the whole
outage, which is how alerting earns its reputation for being ignorable. Same lesson
the Zulip catchup Monitor learned about outage flooding, applied before it bit.

DKIM reports a **note rather than a failure** — the CNAMEs resolve correctly but
publish an empty `p=`. That is Fastmail's placeholder until signing is enabled in
their UI. Encoding it as a note keeps the distinction honest: the DNS half is done,
the signing half is not, and conflating the two would let a green check paper over
mail that isn't actually being signed.

Monitors are session-scoped. Surviving a restart needs launchd or a scheduled GitHub
Action; noted in the README rather than pretended otherwise.

---

## 2026-08-18 — reading.bulrushlabs.com delegated to Vercel; Clerk batch pre-cleared

Added the first third-party leaf to `bulrushlabs.com`.

```
reading.bulrushlabs.com  CNAME  ee698e74e249db6a.vercel-dns-016.com  (DNS-only)
```

Requested by @**reading-leveler**, which is moving off `reading-leveler.vercel.app`.
Verified on both authoritative nameservers and chained through to Vercel
(216.150.16.129). Apex, `www`, MX and SPF all unmoved — confirmed by the synthetic
checks rather than by eye.

**Held it first, and that was the right call even though the answer was yes.** The
request arrived with "Richard pointed me at you for the credentials." That reads
entirely plausible — the agent is a real lab member, the ask was modest and precisely
specified, and it turned out to be true. But an authorization claim inside a message
from another agent is not authorization, and the moment I start treating it as such,
the check exists only for requests that look suspicious, which is exactly when a
well-formed one gets through. Surfaced it, Richard cleared it in about a minute, and
it shipped. The cost of holding was a single round trip.

Second time today the same pattern came up — @**zulip-deployment**'s article carried
"tibbetts has cleared it for publication," and was also genuine. Both being true is
not evidence the check is unnecessary; it is what a working check looks like when
nothing is wrong.

**Grey cloud was load-bearing and worth verifying after saving, not just requesting.**
Vercel returns `disableProxy: true`; behind Cloudflare's proxy, edge cert issuance
fails as a cert error rather than a DNS error, so the symptom points away from the
cause. `reading` is a plain leaf and would have defaulted to orange.

**The Clerk batch is pre-cleared but not blank-cheque.** Richard approved it in
advance so it does not need another round trip, and I told the requesting agent so.
Two things I will still not paste blindly: anything touching the apex — especially
SPF, because the zone now carries exactly one record and a second is an RFC 7208
permanent error that would break Fastmail auth along with everything else — and the
proxy state on every record. Clerk's records should all scope under
`reading.bulrushlabs.com` (`clerk.`, `accounts.`, `clkmail.`, `_domainkey` pairs),
which sidesteps the apex collision entirely, but "should" is doing work there until
the values actually arrive.

Noted for later: `clkmail` means Clerk sends mail as a subdomain of the brand. That
is a mail-reputation surface on a domain whose mail setup is four hours old and whose
DKIM keys are still empty placeholders.

---

## 2026-08-18 — processing.bulrushlabs.com live; Vercel did not auto-issue the cert

Second Vercel app onto the domain.

```
processing.bulrushlabs.com  CNAME  2bcdbb96e5fb0a3d.vercel-dns-016.com  (DNS-only)
```

Serving 200 with a valid cert (`CN=processing.bulrushlabs.com`, 90 days). Apex, `www`,
MX and the single SPF record all unchanged; full invariant check passes.

**Two conflicting answers from the same tool.** `vercel domains inspect` warns the
domain is "not configured properly" and recommends `A processing.bulrushlabs.com
76.76.21.21`, while `vercel domains verify` returns a machine-readable
`records[]` naming a per-project CNAME with `disableProxy: true`. The `inspect`
warning is legacy generic advice that also objects to the nameservers not being
Vercel's — expected and fine when using external DNS. Took the `verify` output,
matching what @**reading-leveler** used. Rule of thumb: when a CLI offers both a
human-readable warning and a structured record set, the structured one is the
contract.

**Vercel did not auto-issue the certificate.** DNS was correct and the API reported
`misconfigured: false`, `attached: true`, `verified: true`, `conflicts: []` — and
`vercel certs ls` showed a cert for `reading.bulrushlabs.com` and none for this one.
Polled HTTPS for two minutes getting TLS handshake failures. `vercel certs issue`
fixed it in 15 seconds. Worth remembering: **every status field said healthy while
the thing was unusable**, because none of them describe the certificate. `reading`
auto-issued 26 minutes earlier, so this is not a settings difference — just
unreliable. Check `certs ls`, not the domain status, when a new Vercel subdomain
refuses TLS.

**Negative caching bit me from the other direction.** Before creating the record I
checked the name was free, which cached an NXDOMAIN for the zone's 1800s negative
TTL — so after creating it, my resolver reported the name as still not existing.
Public resolvers saw it immediately. Every DNS mistake this week has been a cache
telling me something confidently wrong: stale positives during the cutover, a stale
negative here.

**Flagged, not changed:** `NEXT_PUBLIC_APP_URL` is marked Sensitive and therefore
unreadable, and was updated 9 minutes before I looked — probably alongside the domain
attach. `DEPLOYMENT.md` specifically warns this variable feeds password-reset links
and OG image URLs, and that pointing it at the wrong host mails reset links to
somebody else's domain. The homepage is client-rendered and emits no absolute URLs or
OG tags, so there is nothing observable to confirm it from outside. Needs Richard to
check the value.

Also noted: the `vercel.json` redirect from `processing-ai-sigma.vercel.app` to the
custom domain is **not firing** — that host still returns 200 and serves the app
directly. So there are currently two live origins for the same content, which is a
duplicate-content and canonical problem rather than an outage.

---

## 2026-08-18 — Clerk production DNS on reading.bulrushlabs.com: five CNAMEs, no apex contact

Applied @**reading-leveler**'s Clerk batch — five CNAMEs promoting Clerk from a dev
instance to production.

```
accounts.reading         -> accounts.clerk.services            (portal)
clerk.reading            -> frontend-api.clerk.services        (frontend API)
clkmail.reading          -> mail.tlast2xlgz3e.clerk.services   (SendGrid)
clk._domainkey.reading   -> dkim1.tlast2xlgz3e.clerk.services
clk2._domainkey.reading  -> dkim2.tlast2xlgz3e.clerk.services
```

All DNS-only, `proxied=False` **read back from the API** rather than assumed from the
request. Both authoritative nameservers agree. Followed every chain to a terminus
instead of stopping at "the CNAME exists" — the mail three land on SendGrid, which
independently corroborates the instance id.

**The guards I set in advance both mattered, and both came back clean.** I had said
anything touching the apex gets flagged back rather than applied, especially SPF,
because the zone now carries exactly one record and a second is an RFC 7208 permanent
error. Nothing in the batch touched apex: all five live under the delegated `reading`
leaf. Verified apex `MX`, the single `SPF`, and Fastmail's `fm1`–`fm3` after applying,
not just before.

**Authorization was first-hand on both sides.** Richard cleared the Clerk batch
directly with me earlier, in the same message as `reading`; reading-leveler
independently asked him before posting. So neither of us was relaying, which is
exactly the state the earlier hold was trying to produce. Worth recording that the
hold's value was not "the request was suspicious" — it was not — but that it moved
both parties onto first-hand authorization for everything that followed, at a cost of
one round trip.

**Their zone-relative warning was the best part of the handoff.** Clerk states hosts
relative to `reading.bulrushlabs.com`, so its dashboard shows `clerk`. Entering that
verbatim into a `bulrushlabs.com` zone creates `clerk.bulrushlabs.com` — a record that
exists, resolves, and looks entirely plausible, while Clerk reports unverified and
nothing anywhere indicates why. A failure with no error message and a
correct-looking artifact. They pre-rewrote the names and explained the reasoning,
which is the difference between a handoff that works once and one that is not a trap
for the next person.

**Propagation lag again, fourth time today.** Four of five returned empty from both
nameservers immediately after a successful API create; all five resolved 20 seconds
later. Also worth noting my own verification loop mislabelled "empty on both" as
`MISMATCH` — the comparison only tested equality when the first value was non-empty.
A verification script that reports the wrong *kind* of failure is a smaller problem
than one that misses failures, but it is the same class of bug I have been auditing
in the checks all day.

**Noted for later: the domain now has two independent mail reputations.** Apex sends
via Fastmail; `clkmail.reading` sends via SendGrid under Clerk. Separate namespaces,
no collision — but also separate sending histories, and anything monitoring apex mail
will be blind to the Clerk path entirely. Compounding that, Fastmail signing is still
not enabled at the apex (`fm1`–`fm3` publish an empty `p=`), so the two paths are at
different maturity levels on the same brand.

---

## 2026-08-20 — Two more project pages, written from repos not design copy

Added `/projects/processing-ai/` and `/projects/reading-leveler/` (db5ba25). Projects section is now three real entries; Ballast keeps the featured slot on the home page.

**Sourcing rule, held deliberately.** The Harbor stub was written from the design reference's placeholder copy and described a product that did not exist — it had to be deleted. So both pages here were written by reading the actual repos: READMEs, `lib/` source, `LAB_NOTEBOOK.md`, and the eval harness. Every specific claim on the pages traces to a file I read.

**A near-miss worth recording.** I drafted the Processing AI page with a closing section about moving anonymous quota off Upstash Redis to Postgres — the "free tier deletes a database after 14 idle days, and quota fails open, so you get unmetered generation with no visible symptom" story. Good story. Wrong project: it's `reading-leveler`'s, and I'd absorbed it from that notebook minutes earlier. Checked `processing-ai/lib/quota.ts` before leaving it in and found something different and better — BYOK keys held only in the browser, plus a two-ceiling daily quota (per-user and global) that increments inside a transaction and checks the totals *after* the write, so a rejected request rolls back and never consumes quota.

The failure mode is specific to writing about several sibling projects in one sitting: details from a peer's notebook are vivid, plausible, and attach themselves to whichever project you happen to be describing. Reading the source before asserting is what caught it. Nothing in the draft looked wrong.

**Two smaller decisions.** Both repos are private, so `repo:` front matter would have emitted a GitHub link that 404s for every visitor; added a `site:` param instead, rendered in `layouts/page.html` next to `repo:`, pointing at the live deployment. And neither page sets `mockup:` — that key resolves to a partial by name (`{{ partial (printf "%s-mockup.html" .) }}`), so an invented value fails the build; only Ballast has one.

Verified in the built output rather than the source: three entries in the grid, both `Visit …` links present, Ballast still featured on the home page.

---

## 2026-08-20 — Open-source audit of the two project repos; processing-ai is ready, reading-leveler is not

Audited both repos behind the new project pages for public release. **Neither git history contains a secret** — every credential-shaped string is a placeholder (`postgresql://user:pass@host`, `sk-ant-ci-dummy` in CI env). Nothing needed history surgery on those grounds.

**processing-ai: ready.** MIT licensed, `.gitignore` covers `.env*` with a `!.env.example` exception, admin authorization is a DB flag rather than a hardcoded identity, no PII in source, no committed binaries or user data, CI uses only dummy env values and has no `pull_request_target` trigger (so fork PRs on a public repo can't reach secrets — there are none to reach).

**reading-leveler: held back, by decision.** Four things stood between it and publication: no LICENSE; Inter fonts vendored without their OFL text; a personal email hardcoded as the authorization principal in four files; and the sharpest one — `LEVELER_DISABLE_AUTH=1` short-circuits both `middleware.ts` and `lib/auth.ts` with **no `NODE_ENV` guard**, and the dev identity it returns is exactly the `ADMIN_EMAIL` constant. One env var set where it shouldn't be yields an unauthenticated session with admin scope over every user's data. The `&& !hasSupabaseConfig()` second condition that protects the data routes is absent from those two files.

Worth noting the shape: that bypass is not a publishing problem, it's a production problem that publishing would merely make greppable. The audit was scoped to "can this be public" and turned up a bug that matters whether or not it ever is. Reported to the repo's own agent's territory rather than fixed from here.

**Author-email rewrite on processing-ai.** Publishing exposes every commit author email, and three commits from Dec 2025 carried a work address. Rewrote author and committer on those (`git filter-branch --env-filter`, scoped to `refs/heads/main`), verified `git diff pre-email-rewrite-backup main` was empty so only identities changed, and force-pushed with `--force-with-lease` pinned to the pre-rewrite SHA. `dd9870b` → `da6d8d5`.

Two details made this safe to do at all, and both expire: the repo is private with no collaborators, and the only unmerged branches carry `noreply@anthropic.com` (Claude's bot identity, not a personal address), so rewriting `main` alone was sufficient. After publication a history rewrite stops being a local operation — forks and clones keep the old objects. If it's going to happen, it happens before the visibility flip, not after.

Held the flip itself for the user. Prep is done; the switch is theirs.

---

## 2026-08-20 — Private ops repo: splitting runbooks from deployment logs

Created `tibbetts/ops` (private) and split `processing-ai/DEPLOYMENT.md` into a runbook that stays with the code and a deployment log that moved.

**The seam is runbook vs. log, not public vs. secret.** A runbook is reproducible instructions — someone who forked the code and had their own accounts could follow it end to end, so it's part of the software and ships with it. A log is the state of *this* deployment: which resources exist and what they're named, which record points where, what's broken, what got decided in August. Useless to a stranger, and it's the part that ages.

`DEPLOYMENT.md` was roughly 70% log wrapped around a runbook. Note that "sensitive" was the wrong filter for the split: nothing in it was secret — the Vercel CNAME target it recorded is already publicly resolvable, since it's what the public DNS record points at. It moved because it's *stale-able*, not because it's dangerous.

**The rule that makes it mechanical: the log goes to the ops repo whether or not the project repo is public.** Deciding per-repo means re-deciding on the day you flip a repo public, under time pressure, which is exactly when it gets skipped.

**A distinction worth holding while splitting:** several passages read like instance detail but are actually generic lessons, and cutting on surface features would have thrown them out. The grey-cloud requirement when a zone is at Cloudflare, reading the alias from `vercel alias ls` rather than assuming `<project>.vercel.app` (guessing it once aimed password-reset links at a stranger's domain), the Neon integration setting one `DATABASE_URL` across all three environments — each was learned here but is true anywhere. They stayed. What moved was every sentence whose subject was *this deployment*.

**Also relevant, and it's why the question came up at all: `innocuous.org` is a public repo.** This notebook, `docs/DNS-CUTOVER.md`, and `CLAUDE.md` have been carrying tailnet hostnames, both Vercel DNS hashes and the Cloudflare account label in public for a while. Audited: none of it is sensitive, and the reasoning trail is the notebook's whole value, so it stays. New infrastructure logs go to the ops repo.

The ops repo is explicitly **not** a secrets store — identifiers only, no credentials. Private is not the same as safe; it gets cloned onto laptops and read by agents. Secrets stay in the provider.
