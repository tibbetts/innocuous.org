# innocuous.org / Bulrush Labs

Hugo static site. Two things live here at once: the recovered 2005–2015
"Hyperextended Metaphor" WordPress archive, and a Bulrush Labs rebrand built on
top of it.

## Hard requirement: the old URLs must keep working

The original WordPress permalinks are load-bearing — inbound links and search
results still point at them. `hugo.toml` maps them:

- Posts → `/articles/:year/:month/:day/:slug/`
- Categories → `/articles/category/:slug/`, tags → `/articles/tag/:slug/`
- `/tibbetts/` is an alias to `/about/`
- Recovered images are served at their original `/wp-content/uploads/...` paths

Article files are **flat** (`content/articles/2015-05-01-slug.md`) with `slug`
and `date` in front matter; Hugo builds the dated URL. Do not nest them into
`YYYY/MM/DD/` folders — that creates stray section pages for every year, month
and day.

Verify after any config or layout change:

```bash
hugo --gc --minify
ls public/articles/2015/05/01/startups-intellectual-property-boston-inn-of-courts/
```

## Layout

```
content/articles/   # 85 posts (84 recovered + 1 Substack import)
content/projects/   # Bulrush Labs projects (Ballast)
layouts/            # Hugo 0.146+ flat lookup: baseof, home, page, section, term
assets/css/main.css # the whole design layer
assets/img/         # generated brand assets (logo, article thumbnails)
static/wp-content/  # recovered post images at their original paths
archive/wayback/    # raw captures + indexes; NOT published by Hugo
tools/migration/    # recovery scripts — see its README for hard-won details
docs/               # design docs and handoff notes
```

## Conventions

- **Never `rm -rf` inside the working tree.** Use targeted deletes
  (`find content/articles -name '*.md' -delete`) or move a directory aside.
- Front matter keeps `wp_id` and `source_capture` so any post traces back to the
  capture it came from. Preserve them.
- Cross-posted pieces set `canonical` in front matter; that emits `rel=canonical`
  and an "Originally published at" line. Everything else is self-canonical.
- Posts carry a static "Discuss on Hacker News" link (HN Algolia URL search, no
  JavaScript).
- **Link previews are generated, not authored.** `layouts/partials/head-meta.html`
  emits per-page OpenGraph/Twitter tags and draws a 1200×630 card at build time
  (`images.Text` over `assets/img/og-base.png`, using the vendored fonts in
  `assets/fonts/`). Both need Hugo **extended** — CI pins it, so don't unpin it.
  Preview text follows `description` → `summary` → auto-summary → site blurb, so
  a new page gets a real preview by setting `summary` and nothing else. Override
  the image with `image:` in front matter (asset path or absolute URL).
  Regenerate the base canvas with `tools/og/make-base-card.py` if brand colours
  change.

## Deployment

GitHub Actions → GitHub Pages (`.github/workflows/hugo.yml`), currently at
<https://tibbetts.github.io/innocuous.org/>. The build takes its baseURL from
`actions/configure-pages`, so the repo-subpath and a future custom domain both
work. **No `CNAME` is committed** — the DNS cutover for `innocuous.org` is
deliberately a separate step, so the old site is undisturbed.

`main` is the only branch that builds and the only one the `github-pages`
environment permits to deploy. Both halves matter: adding a branch to the
workflow trigger alone will fail at the deploy step, because the environment
restricts branches separately (`gh api repos/:owner/:repo/environments/github-pages/deployment-branch-policies`).

The old `site-redesign` and `bulrush-labs` branches were folded into `main` and
deleted; their history is in `main`. A stale `gh-pages` branch from 2021 still
exists and is *not* in `main`'s history — Pages no longer serves from it
(`build_type: workflow`), but do not delete it without deciding you want that
content gone.

## Local preview

```bash
hugo server --bind 0.0.0.0 --port 1313 --baseURL "http://mini.alewife-bleak.ts.net:1313/"
```

## Lab notebook

Keep `LAB_NOTEBOOK.md` up to date — a dated entry for every meaningful change,
decision, experiment, or dead end, newest at the bottom. Write it as you go, not
at the end. Mirror each entry to the `#innocuous.org-notebook` Zulip channel with
`zulipctl notebook --title "<title>" "<body>"` (one atomic step; see the
`bulrush-labs` and `lab-notebook` skills).
