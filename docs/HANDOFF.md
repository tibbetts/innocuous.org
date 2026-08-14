# Handoff — 14 August 2026

State of the innocuous.org → Bulrush Labs work, written so a fresh session can
pick it up. Background: `docs/superpowers/specs/2026-06-02-innocuous-org-redesign-design.md`
(original redesign plan) and `2026-08-13-bulrush-labs-build-spec.md` (the Diffui
design spec that drove the rebrand).

## Branches

| Branch | What's on it |
|---|---|
| `main` | Only the original README and design doc. Untouched. |
| `site-redesign` | Editorial "Hyperextended Metaphor" design + first 14 posts. **This is what currently deploys to GitHub Pages.** |
| `bulrush-labs` | Everything since: the Bulrush Labs rebrand, all 85 articles, images. **The current work.** |

`bulrush-labs` is branched from `site-redesign`, not merged into anything. No PR
is open.

## Done

- **Full archive recovered from the Wayback Machine.** 85 articles: 84 from
  captures plus one Substack import. Verified complete — every
  `/articles/YYYY/MM/DD/slug/` URL appearing anywhere in the captured HTML has a
  Markdown file. 300 raw captures in `archive/wayback/pages/`.
- **Bulrush Labs redesign** implementing the Diffui reference: masthead, hero,
  featured-project card with a hand-built HTML/CSS product mockup, "Latest from
  the Lab" wired to real posts. Brand assets generated and committed locally.
- **Images self-contained** for everything that survived — 19 post images served
  from `static/wp-content/uploads/` at their original paths.
- **Old URLs preserved and verified** in the built output.
- **CI deploys to GitHub Pages** via Actions.

## Open

1. **The design has never been visually checked.** It was built by reading
   measurements off `assets/design/reference.png` — a safety classifier blocked
   the browser tools for the whole session, so the rendering was never compared
   against the reference. **Highest-value first task: open the preview beside
   that image and diff them.**
2. **`bulrush-labs` doesn't deploy.** Pages still serves the `site-redesign`
   build. To publish it, add the branch to the workflow triggers *and* to the
   `github-pages` environment's allowed branches. Decide first whether the
   rebrand should replace what's public.
3. **14 external images are dead.** Flickr photos from ~2010, 404 on the old
   `farm*.static.flickr.com` hosts, on the `live.staticflickr.com` paths those
   migrated to, and absent from Wayback. Catalogued in
   `archive/wayback/index/external-images.json`. Richard may have the originals.
   The references were left in place deliberately — deleting them would change
   what the posts said.
4. **Content behind the new chrome is thin.** `content/projects/harbor.md` is a
   plausible stub written from the design's copy, not from fact — it needs real
   details or removal. `/notes/` is an empty section. The About page is the
   short `/about/` capture; the fuller "About Richard Tibbetts" text is in
   `archive/wayback/pages/tibbetts/index.html` and was never merged in.
5. **Comments were never extracted.** The design doc wants them in
   `archive/comments/`, shown per-post behind a `show_comments` flag. Captured
   pages show comment *counts* but the threads weren't in the parsed captures.
   This likely needs the WXR export rather than Wayback.
6. **A WXR export is still the better source.** If the origin server behind the
   Cloudflare 522 is reachable, `Tools → Export → All content` gives posts
   Wayback never crawled plus the comment threads. Wayback can only ever return
   what it captured.

## Facts worth not rediscovering

- **2013 and 2014 have no posts, and that is correct.** The site's own Archives
  widget lists no months for those years. Publishing ran Apr 2005 → Feb 2011, a
  single post in Jun 2012, then Mar–May 2015.
- **One page is unrecoverable**: `articles/2009/03/21/hello-world/comment-page-1/`
  — a comment-pagination stub, not an article.
- **The LinkedIn "honey badger" article needs no import.** It is a syndicated
  copy of the 2015 post already recovered, and the recovered version is better —
  it keeps hyperlinks LinkedIn stripped out.
- **The Substack is `tibbetts.substack.com`.** Only one post of consequence,
  already imported.
- `tools/migration/README.md` has the archive.org retrieval lessons — read it
  before touching the fetch scripts.

## Environment

- Hugo v0.165.0 extended (Homebrew). `pandoc` used for HTML→Markdown.
- Preview server, still running from the last session:
  `hugo server --bind 0.0.0.0 --port 1313 --baseURL "http://mini.alewife-bleak.ts.net:1313/"`
- The Diffui auth token in `tools/migration/gen_assets.sh` expires roughly seven
  days after issue; regenerating assets after that needs a fresh build link.
