#!/usr/bin/env python3
"""Re-attempt whatever the main fetch gave up on, cycling candidates harder."""
import json
import os
import random
import subprocess
import time

ROOT = "/Users/tibbetts/code/innocuous.org/archive/wayback"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")

work = {w["path"]: w for w in json.load(open(ROOT + "/index/worklist.json"))}
errors = json.load(open(ROOT + "/index/errors.json"))
manifest = json.load(open(ROOT + "/index/manifest.json"))

still = []
for err in errors:
    it = work.get(err["path"])
    dest = os.path.join(ROOT, err["path"])
    if not it or (os.path.exists(dest) and os.path.getsize(dest) > 200):
        continue
    body = used = None
    for attempt in range(20):
        ts = it["candidates"][attempt % len(it["candidates"])]
        p = subprocess.run(
            ["curl", "-sL", "-A", UA, "--compressed", "--max-time", "90",
             "-w", "\n%{http_code}", "https://web.archive.org/web/%sid_/%s" % (ts, it["url"])],
            capture_output=True)
        out = p.stdout
        nl = out.rfind(b"\n")
        code, data = out[nl + 1:].decode().strip(), out[:nl]
        if code == "200" and len(data) > 200:
            body, used = data, ts
            break
        time.sleep(random.uniform(5, 9))

    if body:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(body)
        manifest[err["path"]] = {"url": it["url"], "ts": used,
                                 "kind": it["kind"], "bytes": len(body)}
        print("RECOVERED %s (%db)" % (err["path"], len(body)), flush=True)
    else:
        still.append(err)
        print("still failing: %s" % err["path"], flush=True)

json.dump(manifest, open(ROOT + "/index/manifest.json", "w"), indent=1)
json.dump(still, open(ROOT + "/index/errors.json", "w"), indent=1)
print("\n%d recovered, %d still failing" % (len(errors) - len(still), len(still)))
