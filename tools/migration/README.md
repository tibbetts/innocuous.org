# Migration tooling

Scripts used to recover innocuous.org from the Wayback Machine and convert it
into Hugo content. Kept because they are re-runnable: all of them are
idempotent and skip work already on disk.

Paths are absolute to `/Users/tibbetts/code/innocuous.org` — adjust `ROOT` /
`REPO` at the top of a script if the repo moves.

## Order of operations

| Script | What it does |
|---|---|
| `worklist.py` | Reads `archive/wayback/index/cdx-all.json` and writes `worklist.json`: one entry per URL with an ordered list of candidate snapshots. |
| `fetch_all.py` | Downloads every work-list URL from Wayback into `archive/wayback/pages/`. Resumable. |
| `retry_failed.py` | Re-attempts whatever `fetch_all.py` recorded in `errors.json`, cycling candidates harder. |
| `fetch_images.py` | Downloads images into `archive/wayback/assets/`, post images first. |
| `extract.py` | Parses every captured page into `content/articles/*.md` via pandoc. |
| `rewrite_images.py` | Publishes recovered uploads to `static/wp-content/uploads/` and repoints posts at them. |
| `extract_substack.py` + `finish_substack.py` | One-off import of a Substack post. Re-usable as a template for other cross-posts. |
| `gen_assets.sh` | Generates the Bulrush Labs design assets via the Diffui API. The auth token in it expires ~7 days after issue. |

Re-running the whole recovery from scratch:

```bash
python3 tools/migration/worklist.py
python3 tools/migration/fetch_all.py       # hours; resumable
python3 tools/migration/retry_failed.py
python3 tools/migration/fetch_images.py
python3 tools/migration/extract.py
python3 tools/migration/rewrite_images.py
hugo --gc --minify
```

## Things learned the hard way

**archive.org's 503s are random load-shedding, not a ban or a dead capture.**
Roughly 25% of replay requests succeed at any spacing. Backing off exponentially
makes throughput *worse* — it multiplies the cost of each retry. Hold a steady
5–8s gap and cycle a URL's candidate snapshots instead. This took the page fetch
from 0.1 pages/min to ~2.4.

**Retry budget should scale with evidence.** A URL with a real CDX capture is
worth 12 attempts; one that only appears as an HTML reference is worth about 3,
because it probably was never crawled. Sorting so that valuable assets come
first matters just as much: alphabetical order put ~120 unarchived photo-album
thumbnails ahead of the article images and wasted hours.

**Follow redirects (`curl -L`).** Wayback answers with 302 to the nearest
capture; without `-L` those look like failures.

**Fetch raw captures with the `id_` modifier** — `/web/<timestamp>id_/<url>` —
which returns the original bytes with no Wayback banner or rewritten URLs.

**Posts appear on more pages than their own.** WordPress renders the same
`<div class="post">` block on the homepage and monthly archives, so a single
homepage capture yielded ten full posts. `extract.py` harvests every capture and
keeps the fullest body per URL.

**Two theme generations.** Later captures use `<div class="post" id="post-N">`;
pre-2007 ones use `<div class="post" onmouseover=...>` with no id. Matching only
the first silently drops the older posts.

**The browser is not a way around the throttling.** A Chrome-driven approach was
tried and abandoned: Wayback's `wombat.js` rewrites `fetch` on replay pages,
Chrome's Local Network Access silently blocks page→localhost requests, and
Wayback sends no CORS headers if you invert the origin. `curl` with the pacing
above is both simpler and faster.
