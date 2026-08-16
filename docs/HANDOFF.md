# Handoff — 14 August 2026

State of the innocuous.org → Bulrush Labs work, written so a fresh session can
pick it up. Background: `docs/superpowers/specs/2026-06-02-innocuous-org-redesign-design.md`
(original redesign plan) and `2026-08-13-bulrush-labs-build-spec.md` (the Diffui
design spec that drove the rebrand).

## Branches

**Superseded as of 16 August 2026.** `bulrush-labs` was fast-forward merged into
`main`, and both `site-redesign` and `bulrush-labs` were deleted — their history
is entirely contained in `main`. There is now one branch, `main`, and it is what
deploys. The table below is kept for context on how the work was originally
split.

| Branch | What was on it |
|---|---|
| `main` | Originally only the README and design doc; now everything. |
| `site-redesign` | Editorial "Hyperextended Metaphor" design + first 14 posts. Deleted. |
| `bulrush-labs` | The Bulrush Labs rebrand, all 85 articles, images. Deleted. |

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
2. ~~**`bulrush-labs` doesn't deploy.**~~ **Done, 14–16 August 2026.** The
   rebrand replaced what's public and now deploys from `main` alone. It needed
   both halves: the branch in the workflow triggers *and* in the `github-pages`
   environment's allowed branches. DNS is still not pointed at it.
3. **14 external images are dead.** Flickr photos from ~2010, 404 on the old
   `farm*.static.flickr.com` hosts, on the `live.staticflickr.com` paths those
   migrated to, and absent from Wayback. Catalogued in
   `archive/wayback/index/external-images.json`. Richard may have the originals.
   The references were left in place deliberately — deleting them would change
   what the posts said.
4. ~~**Content behind the new chrome is thin.**~~ **Done, 14–16 August 2026.**
   Harbor was a stub written from the design's copy rather than fact — the
   product does not exist, so it was removed. `/projects/harbor/` is left to
   404: it only ever existed on the github.io subpath for two days, never at a
   real URL, so it is not one of the load-bearing permalinks.
   Ballast (real, written from the sibling repos)
   took the featured slot, with its own product mockup. `/notes/` became
   `/agent-blog/` with a first post. The fuller "About Richard Tibbetts" text
   was merged from the capture, framed as the 2015 text it is.
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
