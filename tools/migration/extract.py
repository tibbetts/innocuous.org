#!/usr/bin/env python3
"""Harvest posts from every captured page into Hugo content files.

WordPress renders the same `<div class="post">` block on single-post pages,
the homepage and monthly archives, so every capture is a source of posts. Each
post is kept from whichever capture gave the fullest body.
"""
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = "/Users/tibbetts/code/innocuous.org/archive/wayback"
OUT = "/Users/tibbetts/code/innocuous.org/content/articles"

# Older captures use <div class="post" onmouseover=...> with no id.
POST_OPEN = re.compile(r'<div class="post"(?:\s+id="post-(\d+)")?[^>]*>', re.I)
H2_LINK = re.compile(r'<h2>\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>\s*</h2>', re.S | re.I)
H2_PLAIN = re.compile(r"<h2>(.*?)</h2>", re.S | re.I)
DATE = re.compile(r'<span class="date">\s*Posted in\s*(.*?)(?:&not;|¬)\s*(.*?)h?\.?\s*</span>',
                  re.S | re.I)
CATEGORY = re.compile(r'<a[^>]+rel="category tag"[^>]*>(.*?)</a>', re.S | re.I)
TAG = re.compile(r'<a[^>]+rel="tag"[^>]*>(.*?)</a>', re.S | re.I)
DIV = re.compile(r"<(/?)div\b[^>]*>", re.I)


def balanced_div(hay, start):
    """Return the inner HTML of the <div> that starts at `start`."""
    open_tag = hay.find(">", start)
    depth, pos = 1, open_tag + 1
    for m in DIV.finditer(hay, open_tag + 1):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return hay[open_tag + 1:m.start()]
        pos = m.end()
    return hay[open_tag + 1:pos]


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def parse_date(datestr, timestr):
    txt = strip_tags(html.unescape(datestr)).strip(" ,")
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            d = datetime.strptime(txt, fmt)
            break
        except ValueError:
            d = None
    if not d:
        return None
    t = strip_tags(html.unescape(timestr or "")).lower().replace(" ", "")
    m = re.match(r"(\d{1,2}):(\d{2})(am|pm)?", t)
    if m:
        hh, mm = int(m.group(1)), int(m.group(2))
        if m.group(3) == "pm" and hh != 12:
            hh += 12
        if m.group(3) == "am" and hh == 12:
            hh = 0
        d = d.replace(hour=hh, minute=mm)
    return d


def harvest(path, page_url):
    """Yield every post block found in one captured page."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    for m in POST_OPEN.finditer(raw):
        block = balanced_div(raw, m.start())
        link = H2_LINK.search(block)
        if link:
            permalink, title = link.group(1), strip_tags(link.group(2))
        else:
            plain = H2_PLAIN.search(block)
            if not plain:
                continue
            permalink, title = page_url, strip_tags(plain.group(1))
        permalink = re.sub(r"^https?://web\.archive\.org/web/\d+[a-z_]*/", "", permalink)

        ent = re.search(r'<div class="entry">', block, re.I)
        body = balanced_div(block, ent.start()) if ent else ""

        dm = DATE.search(block)
        when = parse_date(dm.group(1), dm.group(2)) if dm else None

        meta = block[ent.end():] if ent else block
        yield {
            "id": m.group(1) or "0",
            "permalink": permalink,
            "title": html.unescape(title),
            "date": when.isoformat() if when else None,
            "categories": [html.unescape(strip_tags(c)) for c in CATEGORY.findall(meta)],
            "tags": [html.unescape(strip_tags(t)) for t in TAG.findall(meta)],
            "body_html": body.strip(),
            "source": os.path.relpath(path, ROOT),
        }


def slug_parts(permalink):
    m = re.search(r"/articles/(\d{4})/(\d{2})/(\d{2})/([^/?#]+)", permalink)
    return m.groups() if m else None


def to_markdown(body_html):
    p = subprocess.run(
        ["pandoc", "-f", "html", "-t", "markdown_strict-raw_html", "--wrap=none"],
        input=body_html.encode(), capture_output=True,
    )
    if p.returncode != 0:
        return None
    return p.stdout.decode()


def yaml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    manifest = json.load(open(ROOT + "/index/manifest.json"))
    best = {}
    for relpath, meta in sorted(manifest.items()):
        full = os.path.join(ROOT, relpath)
        if not os.path.exists(full):
            continue
        for post in harvest(full, meta["url"]):
            parts = slug_parts(post["permalink"])
            if not parts:
                continue
            key = "/".join(parts)
            # Listing pages can carry excerpts; keep the fullest body seen.
            if key not in best or len(post["body_html"]) > len(best[key]["body_html"]):
                best[key] = post

    os.makedirs(OUT, exist_ok=True)
    written = skipped = 0
    for key, post in sorted(best.items()):
        y, mo, d, slug = key.split("/")
        md = to_markdown(post["body_html"])
        if md is None:
            skipped += 1
            continue
        fm = ["---",
              "title: " + yaml_str(post["title"]),
              "date: " + (post["date"] or "%s-%s-%sT00:00:00" % (y, mo, d)),
              "slug: " + yaml_str(slug),
              "wp_id: " + post["id"]]
        if post["categories"]:
            fm.append("categories:")
            fm += ["  - " + yaml_str(c) for c in dict.fromkeys(post["categories"])]
        if post["tags"]:
            fm.append("tags:")
            fm += ["  - " + yaml_str(t) for t in dict.fromkeys(post["tags"])]
        fm += ["source_capture: " + yaml_str(post["source"]), "---", ""]

        # Flat files: Hugo builds the dated permalink from front matter, so
        # nested folders would only create stray section pages.
        dest = os.path.join(OUT, "%s-%s-%s-%s.md" % (y, mo, d, slug))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w") as fh:
            fh.write("\n".join(fm) + md.strip() + "\n")
        written += 1

    print("harvested %d unique posts from %d captures" % (len(best), len(manifest)))
    print("wrote %d markdown files, %d skipped" % (written, skipped))
    years = {}
    for k in best:
        years[k[:4]] = years.get(k[:4], 0) + 1
    print("by year:", dict(sorted(years.items())))


if __name__ == "__main__":
    main()
