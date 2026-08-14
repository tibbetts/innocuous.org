#!/usr/bin/env python3
"""Build the work list: per URL, an ordered list of candidate snapshots.

Some Wayback captures are permanently 503 (their WARC is unreachable), so each
URL carries fallbacks — newest usable capture first, truncated ones last.
"""
import json
import re
import collections
from urllib.parse import urlsplit, urlunsplit

ROOT = "/Users/tibbetts/code/innocuous.org/archive/wayback"

rows = json.load(open(ROOT + "/index/cdx-all.json"))
hdr, rows = rows[0], rows[1:]
I = {n: i for i, n in enumerate(hdr)}

SKIP = re.compile(r"/dashboard/|/wp-login\.php")
MAX_CANDIDATES = 8


def norm(u):
    s = urlsplit(u)
    host = re.sub(r"^www\.", "", s.netloc.lower().replace(":80", ""))
    p = re.sub(r"/{2,}", "/", s.path or "/")
    if not p.endswith("/") and "." not in p.rsplit("/", 1)[-1]:
        p += "/"
    return urlunsplit(("", host, p, s.query, ""))


def kind(u):
    if re.search(r"/articles/\d{4}/\d{2}/\d{2}/", u):
        return "post"
    if "/articles/category/" in u:
        return "category"
    if "/articles/tag/" in u:
        return "tag"
    if re.search(r"/articles/\d{4}/", u):
        return "archive"
    return "page"


def savepath(u):
    s = urlsplit(u)
    rel = re.sub(r"/{2,}", "/", s.path).strip("/") or "index"
    if s.query:
        rel += "__" + re.sub(r"[^A-Za-z0-9._-]+", "_", s.query)[:80]
    if re.search(r"\.(html|cgi|php)$", rel):
        rel = rel.rsplit(".", 1)[0] + ".html"
    else:
        rel += "/index.html"
    return "pages/" + rel


by = collections.defaultdict(list)
for r in rows:
    n = norm(r[I["original"]])
    if SKIP.search(n):
        continue
    by[n].append(r)

work = []
for u, snaps in sorted(by.items()):
    lens = {s[I["timestamp"]]: int(s[I["length"]] or 0) for s in snaps}
    best = max(lens.values()) or 1
    ts_all = sorted(lens, reverse=True)
    full = [t for t in ts_all if lens[t] >= 0.5 * best]
    partial = [t for t in ts_all if lens[t] < 0.5 * best]
    work.append({
        "url": "http://" + u.lstrip("/"),
        "kind": kind(u),
        "path": savepath(u),
        "candidates": (full + partial)[:MAX_CANDIDATES],
        "snaps": len(snaps),
    })

json.dump(work, open(ROOT + "/index/worklist.json", "w"), indent=1)
counts = collections.Counter(w["kind"] for w in work)
multi = sum(1 for w in work if len(w["candidates"]) > 1)
print("work items:", len(work), dict(counts))
print("with fallbacks:", multi, "| single-candidate:", len(work) - multi)
print("avg candidates: %.1f" % (sum(len(w["candidates"]) for w in work) / len(work)))
