#!/usr/bin/env python3
"""Convert the saved Substack post into a Hugo content file."""
import html
import json
import re
import subprocess

SRC = "/private/tmp/claude-501/-Users-tibbetts-code-innocuous-org/c98e9257-b3a4-4d3a-b5b5-98025b022588/scratchpad/substack.html"
OUT = "/private/tmp/claude-501/-Users-tibbetts-code-innocuous-org/c98e9257-b3a4-4d3a-b5b5-98025b022588/scratchpad/substack-post.md"

raw = open(SRC, encoding="utf-8", errors="replace").read()
DIV = re.compile(r"<(/?)div\b[^>]*>", re.I)


def balanced(hay, start):
    open_tag = hay.find(">", start)
    depth = 1
    for m in DIV.finditer(hay, open_tag + 1):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return hay[open_tag + 1:m.start()]
    return ""


# Title: prefer the on-page post heading over the publication name.
title = None
m = re.search(r'<h1[^>]*class="[^"]*post-title[^"]*"[^>]*>(.*?)</h1>', raw, re.S)
if m:
    title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
if not title:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "Untitled"

sub = None
m = re.search(r'"subtitle":"((?:[^"\\]|\\.)*)"', raw)
if m:
    sub = json.loads('"%s"' % m.group(1)) or None

date = None
m = re.search(r'"post_date":"([^"]+)"', raw) or re.search(r'"datePublished":"([^"]+)"', raw)
if m:
    date = m.group(1)

canon = None
m = re.search(r'<meta property="og:url" content="([^"]+)"', raw)
if m:
    canon = m.group(1)

# Body
m = re.search(r'<div[^>]*class="[^"]*body markup[^"]*"[^>]*>', raw)
body = balanced(raw, m.start()) if m else ""

# Strip Substack's own furniture before converting.
# Drop Substack's inline subscribe forms, which sit inside the body div.
body = re.sub(r'<div[^>]*data-component-name="SubscribeWidget".*?</form>.*?</div></div></div>',
              "", body, flags=re.S)
body = re.sub(r"<form\b.*?</form>", "", body, flags=re.S)
body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.S)
body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.S)

p = subprocess.run(
    ["pandoc", "-f", "html", "-t", "markdown_strict-raw_html", "--wrap=none"],
    input=body.encode(), capture_output=True)
md = p.stdout.decode().strip()

print("title:", title)
print("subtitle:", sub)
print("date:", date)
print("canonical:", canon)
print("body chars:", len(body), "-> markdown chars:", len(md))
print("paywall truncated?", "yes" if len(md) < 400 else "no")

fm = ["---", 'title: "%s"' % title.replace('"', '\\"')]
if sub:
    fm.append('summary: "%s"' % sub.replace('"', '\\"'))
if date:
    fm.append("date: %s" % date[:19])
fm += ['slug: "the-best-resting-and-vesting"',
       'canonical: "%s"' % canon,
       'source: "substack"', "---", ""]
open(OUT, "w").write("\n".join(fm) + md + "\n")
print("\nwrote", OUT)
print("\n--- first 600 chars of body ---")
print(md[:600])
