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
