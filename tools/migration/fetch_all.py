#!/usr/bin/env python3
"""Fetch every work-list URL from the Wayback Machine, rate-limit aware.

The 503s are archive.org throttling, not dead captures, so the pacing adapts:
the gap between requests grows on 503 and relaxes on success. Sequential and
resumable — safe to re-run to mop up whatever failed.
"""
import json
import os
import random
import subprocess
import sys
import time

ROOT = "/Users/tibbetts/code/innocuous.org/archive/wayback"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")

COOLDOWN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0

work = json.load(open(ROOT + "/index/worklist.json"))
manifest_path = ROOT + "/index/manifest.json"
manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
errors = []
ok = skipped = failed = 0

delay = 8.0          # adaptive gap between requests
consecutive_503 = 0
t0 = time.time()

if COOLDOWN:
    print("cooling down %.0fs before starting..." % COOLDOWN, flush=True)
    time.sleep(COOLDOWN)


def fetch(url):
    p = subprocess.run(
        ["curl", "-sL", "-A", UA, "--compressed", "--max-time", "90",
         "-w", "\n%{http_code}", url],
        capture_output=True,
    )
    out = p.stdout
    nl = out.rfind(b"\n")
    return out[nl + 1:].decode().strip(), out[:nl]


def pace(hit_limit):
    """Steady pacing.

    The 503s are random load-shedding (~25% of requests succeed at any spacing),
    not an escalating penalty, so backing off just multiplies the cost of each
    retry. Hold a modest constant gap and only rest if it goes truly cold.
    """
    global consecutive_503
    if hit_limit:
        consecutive_503 += 1
        if consecutive_503 and consecutive_503 % 40 == 0:
            print("   ...gone cold, resting 2 min", flush=True)
            time.sleep(120)
    else:
        consecutive_503 = 0
    time.sleep(random.uniform(5, 8))


for i, it in enumerate(work, 1):
    dest = os.path.join(ROOT, it["path"])
    if os.path.exists(dest) and os.path.getsize(dest) > 200:
        skipped += 1
        continue

    # Cycle the candidates repeatedly: with ~25% success per request, a given
    # capture usually serves within a few tries.
    body = used = None
    tried = []
    cands = it["candidates"] or []
    for attempt in range(14):
        ts = cands[attempt % len(cands)]
        code, data = fetch("https://web.archive.org/web/%sid_/%s" % (ts, it["url"]))
        if code == "200" and len(data) > 200:
            body, used = data, ts
            pace(False)
            break
        tried.append("%s:%s" % (ts, code))
        pace(code in ("503", "429"))

    if body is None:
        failed += 1
        errors.append({"path": it["path"], "url": it["url"], "tried": tried})
        print("[%d/%d] FAIL %s (%s)" % (i, len(work), it["path"][:50],
                                        ",".join(tried[:4])), flush=True)
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(body)
        manifest[it["path"]] = {"url": it["url"], "ts": used, "kind": it["kind"],
                                "bytes": len(body)}
        ok += 1
        rate = ok / max((time.time() - t0) / 60, 0.01)
        print("[%d/%d] %-8s %-46s %6db gap=%.0fs %.1f/min"
              % (i, len(work), it["kind"], it["path"][:46], len(body), delay, rate),
              flush=True)
        json.dump(manifest, open(manifest_path, "w"), indent=1)

json.dump(errors, open(ROOT + "/index/errors.json", "w"), indent=1)
print("\nDONE in %.1f min — %d saved, %d skipped, %d failed"
      % ((time.time() - t0) / 60, ok, skipped, failed))
