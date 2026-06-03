# innocuous.org Redesign — Design Doc

**Date:** 2026-06-02
**Status:** Approved (design), pending spec review
**Author:** Richard Tibbetts (with Claude)

## Summary

Rebuild **innocuous.org** as a [Hugo](https://gohugo.io) static site, deployed to
GitHub Pages via GitHub Actions. Faithfully migrate the full ~10-year
"Hyperextended Metaphor" WordPress archive (2005–2015), **preserving existing
`/articles/YYYY/MM/DD/slug/` permalinks**, and add a light landing/about presence
on top of the blog. Establish a clean Hugo project and local/CI build workflow —
"the place for building" the new site.

## Background / current state

- The repo `tibbetts/innocuous.org` currently has two branches:
  - `main` — only `README.md` and a Jekyll-oriented `.gitignore`.
  - `gh-pages` — the **default GitHub Pages template** (slate theme, placeholder
    `index.md`, title with a typo "Hyperexteneded Metaphor").
- The **real** site is a **WordPress 2.9.2** blog (`dfblog` theme) titled
  **"Hyperextended Metaphor — Richard Tibbetts on Various Topics"**, currently
  unreachable (Cloudflare 522 in front of the origin). Content recovered/observed
  via the Wayback Machine (snapshot 2022-07-09):
  - ~10 years of posts, **monthly archives April 2005 → May 2015**.
  - Categories: Books, Business, Management, Miscellaneous, Politics, Technology.
  - An **"About Richard Tibbetts"** page at `/tibbetts/`.
  - Permalink structure: `/articles/YYYY/MM/DD/slug/`, plus
    `/articles/category/...` and `/articles/tag/...`.
  - Comments were enabled on posts.
- The site owner has (likely) admin access to the live WordPress server.

## Goals

1. New site built with **Hugo**, deployed to **GitHub Pages via GitHub Actions**.
2. Migrate **all** existing posts and the About page.
3. **Preserve `/articles/YYYY/MM/DD/slug/` permalinks** and old taxonomy URLs so
   inbound links and search results keep working.
4. Add a light **landing/about** layer (blog + light portfolio/landing).
5. Provide a clean repo layout + local dev + CI for ongoing iteration.

## Non-goals

- No WordPress upgrade or any dynamic backend.
- No live, on-page commenting system.
- No bespoke theme built from scratch in v1 (start from a minimal theme, customize).
- No full rebrand beyond "modern, clean, readable."

## Architecture & decisions

### Stack & hosting

- **Hugo** — single Go binary, no dependency rot, fast builds over hundreds of
  posts, first-class permalink/taxonomy control.
- **Source of truth on `main`**; a **GitHub Actions** workflow builds Hugo and
  publishes to Pages (the modern, recommended approach — replaces the legacy
  native-Jekyll build, which is version-frozen with a limited plugin allow-list).
- **Retire the current `gh-pages` template branch**: back up its two files first,
  then set Pages "Build and deployment → Source" to **GitHub Actions**.
- **Custom domain** `innocuous.org` via a `CNAME` file / Pages domain config.

### Repo structure

```
/                          # main branch = Hugo source
├── hugo.toml              # config: baseURL, permalinks, taxonomies
├── content/
│   ├── _index.md          # landing/home
│   ├── about.md           # "About Richard Tibbetts" (was /tibbetts/)
│   └── articles/          # migrated posts (dated front matter)
├── layouts/               # template overrides (incl. "Discuss on HN" partial)
├── assets/                # css/js pipeline
├── static/                # migrated uploads/images, CNAME
├── archive/               # raw export (WXR or SQL) + extracted comments — NOT published
├── .github/workflows/     # build + deploy to GitHub Pages
└── docs/superpowers/specs/ # design docs
```

### Content migration

Two source paths, both converging on Hugo Markdown:

- **Preferred — WXR export:** owner runs **Tools → Export → All content** in the
  live WordPress (available even in 2.9.2), producing a WXR XML file. Convert with
  **`wordpress-export-to-markdown`** (Node tool, run once locally and discarded):
  generates dated Markdown + front matter and can download/rewrite image URLs.
  (Chosen over the WP-side Hugo exporter plugin, which won't run on a 2010-era
  WordPress.)
- **Fallback — SQL dump:** if only a MySQL dump is available, load it into a local
  throwaway MySQL, then either (a) run WordPress locally long enough to produce a
  WXR export, or (b) run a script against `wp_posts` / `wp_postmeta` /
  `wp_terms` / `wp_term_relationships` / `wp_comments` to emit Hugo Markdown
  directly. More work, fully doable.

Images: also fetch `wp-content/uploads/` if reachable. **Default: host images
in-repo under `static/`** so the site is self-contained. (Open: could keep an
external URL instead.)

I will spot-review a sample of converted posts for HTML→Markdown fidelity before
bulk-committing.

### Permalink preservation (hard requirement)

- Hugo `permalinks` config renders the `articles` section as
  `/articles/:year/:month/:day/:slug/` — matching WordPress exactly.
- Each post also gets `aliases` for URL variations as a 404 safety net.
- Taxonomy pages mapped to `/articles/category/...` and `/articles/tag/...`.
- A **link-check pass** validates the new site against the captured list of old
  archive URLs before cutover.

### Comments

- The export includes all comments. Extract them into `archive/comments/`
  (one file per post) as a preserved record — **not rendered on pages by default.**
- **Selective display:** for posts with a genuinely strong thread, render comments
  via a per-post front-matter flag (e.g. `show_comments: true`). Owner chooses
  during review.
- **Future discussion → Hacker News:** a static template partial adds a
  **"Discuss on Hacker News"** link to each post. **Default:** link to the HN
  Algolia search-by-URL (`https://hn.algolia.com/?query={permalink}`) — works
  whether or not a thread exists yet, zero JavaScript. (Alternative submit link:
  `https://news.ycombinator.com/submitlink?u={permalink}&t={title}`.)

### Design direction

- Start from a **well-built minimal Hugo theme** (Congo / PaperMod-style: clean
  typography, light/dark, fast) and customize lightly rather than building from
  scratch.
- **Home:** short landing/about intro + recent posts. **About:** carried over.
  **Blog:** archive with category/tag browsing.
- Specific theme/visual direction chosen at build time (frontend-design skill).

### Domain / DNS cutover (operational, deploy-day)

- The old site stays up until cutover; this step is reversible.
- When ready, point DNS/Cloudflare at GitHub Pages and configure the custom domain
  + HTTPS in repo settings. Called out separately so the old site isn't broken
  prematurely.

## Risks & open items

- **Export availability:** WXR export may be blocked → SQL-dump fallback (above).
- **Conversion fidelity:** 16-year-old WordPress HTML may need spot fixes; budgeted
  into the migration step.
- **Open sub-decisions (resolved at build time):** image hosting (in-repo vs
  external); specific theme/visual direction; exact HN link flavor.

## Success criteria

- New Hugo site builds in CI and deploys to GitHub Pages.
- All migrated posts + About page render correctly at their **original
  `/articles/YYYY/MM/DD/slug/` URLs**; link-check passes against the old URL list.
- Comments preserved in `archive/`, shown only where flagged.
- Each post offers a working "Discuss on HN" link.
- Local dev (`hugo server`) and CI build both work from a clean checkout.
