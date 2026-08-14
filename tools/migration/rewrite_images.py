#!/usr/bin/env python3
"""Point the migrated posts at locally hosted images.

Recovered uploads are published at their original /wp-content/uploads/... path,
so old inbound image links keep resolving for the same reason the article
permalinks do. Externally hosted images are left alone — they belong to other
sites.
"""
import glob
import os
import re
import shutil
from urllib.parse import urlsplit, unquote

REPO = "/Users/tibbetts/code/innocuous.org"
SRC = REPO + "/archive/wayback/assets/wp-content/uploads"
DST = REPO + "/static/wp-content/uploads"

# 1. publish the recovered uploads
copied = 0
for dirpath, _, files in os.walk(SRC):
    for fn in files:
        s = os.path.join(dirpath, fn)
        rel = os.path.relpath(s, SRC)
        d = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if not os.path.exists(d) or os.path.getsize(d) != os.path.getsize(s):
            shutil.copy2(s, d)
            copied += 1
print("published %d upload files to static/wp-content/uploads" % copied)

have = set()
for dirpath, _, files in os.walk(DST):
    for fn in files:
        have.add("/" + os.path.relpath(os.path.join(dirpath, fn), REPO + "/static"))

# 2. rewrite references in the posts
IMG = re.compile(r'(!\[[^\]]*\]\()([^)\s]+)')
rewritten = missing = external = 0
missing_list = []

for f in sorted(glob.glob(REPO + "/content/articles/*.md")):
    text = open(f, encoding="utf-8").read()
    orig = text

    def fix(m):
        global rewritten, missing, external
        head, url = m.group(1), m.group(2)
        s = urlsplit(url)
        host = s.netloc.lower().replace(":80", "").replace("www.", "")
        if host and host != "innocuous.org":
            external += 1
            return m.group(0)
        if not s.path.startswith("/wp-content/uploads"):
            return m.group(0)
        local = unquote(s.path)
        if local in have:
            rewritten += 1
            return head + local
        missing += 1
        missing_list.append((os.path.basename(f), s.path))
        return m.group(0)

    text = IMG.sub(fix, text)
    if text != orig:
        open(f, "w").write(text)

print("rewritten to local: %d | still remote (external hosts): %d | missing locally: %d"
      % (rewritten, external, missing))
for f, p in missing_list:
    print("   MISSING %-46s %s" % (f[:46], p))
