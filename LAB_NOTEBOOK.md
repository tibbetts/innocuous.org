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
