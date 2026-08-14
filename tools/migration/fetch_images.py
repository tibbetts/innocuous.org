#!/usr/bin/env python3
"""Fetch images for the archived site.

Sources are unioned: images Wayback indexed (cdx-assets.json) plus every image
actually referenced by the downloaded HTML — the latter catches files the
crawler never indexed but may still hold. Skips wp-admin and theme chrome,
which the new Hugo theme won't need.
"""
import json
import os
import random
import re
import subprocess
import time
from urllib.parse import urljoin, urlsplit

ROOT = "/Users/tibbetts/code/innocuous.org/archive/wayback"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")

IMG_EXT = re.compile(r"\.(png|jpe?g|gif|svg|ico|bmp|webp)(\?|$)", re.I)
SKIP = re.compile(r"/wp-admin/|/wp-content/themes/|/wp-includes/")
SRC = re.compile(rb"""<img[^>]+src\s*=\s*["']([^"']+)["']""", re.I)
HREF = re.compile(rb"""<a[^>]+href\s*=\s*["']([^"']+\.(?:png|jpe?g|gif))["']""", re.I)

manifest = json.load(open(ROOT + "/index/manifest.json"))

# --- 1. images referenced by the pages we actually downloaded -----------------
referenced = {}   # url -> set of pages referencing it
external = {}
for relpath, meta in manifest.items():
    full = os.path.join(ROOT, relpath)
    if not os.path.exists(full):
        continue
    html = open(full, "rb").read()
    for m in list(SRC.findall(html)) + list(HREF.findall(html)):
        try:
            raw = m.decode("utf-8", "replace").strip()
        except Exception:
            continue
        if raw.startswith("data:"):
            continue
        # Strip any Wayback prefix that survived in the markup.
        raw = re.sub(r"^https?://web\.archive\.org/web/\d+[a-z_]*/", "", raw)
        absu = urljoin(meta["url"], raw)
        if not absu.startswith("http"):
            continue
        host = urlsplit(absu).netloc.lower().replace(":80", "")
        if not IMG_EXT.search(absu):
            continue
        if host.replace("www.", "") != "innocuous.org":
            external.setdefault(absu, []).append(relpath)
            continue
        if SKIP.search(absu):
            continue
        referenced.setdefault(absu, []).append(relpath)

# --- 2. images Wayback indexed ----------------------------------------------
rows = json.load(open(ROOT + "/index/cdx-assets.json"))[1:]
snaps = {}
for ts, orig, code, mime, length in rows:
    if not mime.startswith("image/"):
        continue
    snaps.setdefault(orig, []).append(ts)
indexed = {u for u in snaps if not SKIP.search(u)}


def key(u):
    """Match a referenced URL to CDX entries despite www/:80 variance."""
    s = urlsplit(u)
    return re.sub(r"^www\.", "", s.netloc.lower().replace(":80", "")) + s.path


snap_by_key = {}
for u, ts in snaps.items():
    snap_by_key.setdefault(key(u), []).extend(ts)

def priority(u):
    if "/wp-content/uploads" in u:
        return (0, u)      # article imagery — the assets that matter
    if "/photos/" in u:
        return (2, u)
    return (1, u)


targets = sorted(set(referenced) | indexed, key=priority)
print("referenced by pages: %d | indexed by wayback: %d | union: %d"
      % (len(referenced), len(indexed), len(targets)))


def savepath(u):
    s = urlsplit(u)
    rel = re.sub(r"/{2,}", "/", s.path).strip("/") or "index"
    return "assets/" + rel


def fetch(url):
    p = subprocess.run(
        ["curl", "-s", "-A", UA, "--compressed", "--max-time", "90",
         "-w", "\n%{http_code}", url],
        capture_output=True,
    )
    out = p.stdout
    nl = out.rfind(b"\n")
    return out[nl + 1:].decode().strip(), out[:nl]


img_manifest = {}
errors = []
ok = skipped = failed = 0
t0 = time.time()

for i, u in enumerate(targets, 1):
    dest = os.path.join(ROOT, savepath(u))
    if os.path.exists(dest) and os.path.getsize(dest) > 100:
        skipped += 1
        continue

    # Newest captures first; "2015id_" lets Wayback choose when we have no index.
    real = sorted(set(snap_by_key.get(key(u), [])), reverse=True)[:6]
    cands = real or ["2015"]
    # Unindexed URLs almost certainly were never captured; don't burn 12 tries.
    budget = 12 if real else 3
    body = used = None
    tried = []
    misses = 0
    # 503 means archive.org is shedding load, so retry; 404 means the capture
    # genuinely isn't there, so give up on it quickly.
    for attempt in range(budget):
        ts = cands[attempt % len(cands)]
        code, data = fetch("https://web.archive.org/web/%sid_/%s" % (ts, u))
        if code == "200" and len(data) > 100:
            body, used = data, ts
            break
        tried.append("%s:%s" % (ts, code))
        if code == "404":
            misses += 1
            if misses >= len(cands):
                break
        time.sleep(random.uniform(4, 7))

    if body is None:
        failed += 1
        errors.append({"url": u, "tried": tried,
                       "referenced_by": referenced.get(u, [])[:3]})
        print("[%d/%d] FAIL %s (%s)" % (i, len(targets), u[:70], ",".join(tried[:4])),
              flush=True)
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(body)
        img_manifest[savepath(u)] = {"url": u, "ts": used, "bytes": len(body),
                                     "referenced_by": referenced.get(u, [])}
        ok += 1
        print("[%d/%d] %-62s %7db" % (i, len(targets), savepath(u)[:62], len(body)),
              flush=True)
        time.sleep(random.uniform(1.2, 3.0))

json.dump(img_manifest, open(ROOT + "/index/image-manifest.json", "w"), indent=1)
json.dump(errors, open(ROOT + "/index/image-errors.json", "w"), indent=1)
json.dump(external, open(ROOT + "/index/external-images.json", "w"), indent=1)
print("\nDONE in %.1f min — %d saved, %d skipped, %d failed, %d external (recorded)"
      % ((time.time() - t0) / 60, ok, skipped, failed, len(external)))
