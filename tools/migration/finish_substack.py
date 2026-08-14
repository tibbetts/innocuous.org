#!/usr/bin/env python3
"""Clean the converted Substack post and install it as a Hugo article."""
import re
import subprocess
import os

SRC = "/private/tmp/claude-501/-Users-tibbetts-code-innocuous-org/c98e9257-b3a4-4d3a-b5b5-98025b022588/scratchpad/substack-post.md"
REPO = "/Users/tibbetts/code/innocuous.org"
IMGDIR = REPO + "/static/img/posts"
DEST = REPO + "/content/articles/2023-06-30-the-best-resting-and-vesting.md"
LOCAL_IMG = "/img/posts/resting-vesting.jpg"

text = open(SRC, encoding="utf-8").read()
fm, body = text.split("---\n", 2)[1], text.split("---\n", 2)[2]

# Substack ships base64 SVG spacers for lazy loading; they are not content.
body = re.sub(r"!\[[^\]]*\]\(data:image/[^)]*\)\s*", "", body)

# Pull the one real image local rather than hotlinking the Substack CDN.
# pandoc emits ![alt](url "title"), so stop the URL at the first space.
imgs = re.findall(r'!\[([^\]]*)\]\((https://substackcdn\.com[^)\s]+)', body)
os.makedirs(IMGDIR, exist_ok=True)
if imgs:
    alt, url = imgs[0]
    subprocess.run(["curl", "-sSL", "--max-time", "120", "-o",
                    IMGDIR + "/resting-vesting.jpg", url], check=False)
    size = os.path.getsize(IMGDIR + "/resting-vesting.jpg")
    print("image downloaded: %d bytes" % size)
    body = re.sub(r'!\[([^\]]*)\]\(https://substackcdn\.com[^)]*\)',
                  lambda m: "![%s](%s)" % (m.group(1).strip(), LOCAL_IMG), body)

# The page title is the h1, so in-body headings start at h2.
body = re.sub(r"^# ", "## ", body, flags=re.M)

# Collapse the blank lines the stripped placeholders left behind.
body = re.sub(r"\n{3,}", "\n\n", body).strip()

front = """---
title: "Making the Best of Your Time Resting and Vesting"
date: 2023-06-30T21:07:17
slug: "the-best-resting-and-vesting"
categories:
  - "Business"
  - "Management"
canonical: "https://tibbetts.substack.com/p/the-best-resting-and-vesting"
source_note: "Originally published on Substack"
---

"""

open(DEST, "w").write(front + body + "\n")
print("wrote", DEST)
print("words:", len(body.split()))
print("remaining data: URIs:", body.count("data:image"))
print("remaining substackcdn refs:", body.count("substackcdn"))
