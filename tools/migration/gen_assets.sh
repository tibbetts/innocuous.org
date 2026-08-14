#!/bin/bash
# Generate the design's illustrative assets via Diffui, then download them
# locally (auth tokens expire, so nothing is hotlinked).
set -u
TOKEN="6r1bcfJAIzlg"
OUT=/Users/tibbetts/code/innocuous.org/assets/img
TMP=/private/tmp/claude-501/-Users-tibbetts-code-innocuous-org/c98e9257-b3a4-4d3a-b5b5-98025b022588/scratchpad/gen
mkdir -p "$OUT" "$TMP"

gen_image() {
  local name="$1" prompt="$2" w="$3" h="$4"
  curl -sS --max-time 420 -X POST https://diffui.ai/api/build/generate-image \
    -H "Content-Type: application/json" \
    -d "$(python3 -c '
import json,sys
print(json.dumps({"authToken":sys.argv[1],"prompt":sys.argv[2],
                  "width":int(sys.argv[3]),"height":int(sys.argv[4]),"quality":"medium"}))
' "$TOKEN" "$prompt" "$w" "$h")" > "$TMP/$name.json" 2>&1
  local url
  url=$(python3 -c "
import json
try: print(json.load(open('$TMP/$name.json')).get('url',''))
except Exception: print('')
")
  if [ -n "$url" ]; then
    curl -sSL --max-time 300 -o "$OUT/$name.webp" "$url"
    echo "OK   $name -> $(wc -c < "$OUT/$name.webp") bytes"
  else
    echo "FAIL $name: $(head -c 200 "$TMP/$name.json")"
  fi
}

gen_svg() {
  local name="$1" prompt="$2" instr="$3"
  curl -sS --max-time 420 -X POST https://diffui.ai/api/build/generate-svg \
    -H "Content-Type: application/json" \
    -d "$(python3 -c '
import json,sys
print(json.dumps({"authToken":sys.argv[1],"prompt":sys.argv[2],"instructions":sys.argv[3],
                  "viewBox":{"minX":0,"minY":0,"width":64,"height":64}}))
' "$TOKEN" "$prompt" "$instr")" > "$TMP/$name.json" 2>&1
  local url
  url=$(python3 -c "
import json
try: print(json.load(open('$TMP/$name.json')).get('url',''))
except Exception: print('')
")
  if [ -n "$url" ]; then
    curl -sSL --max-time 300 -o "$OUT/$name.svg" "$url"
    echo "OK   $name -> $(wc -c < "$OUT/$name.svg") bytes"
  else
    echo "FAIL $name: $(head -c 200 "$TMP/$name.json")"
  fi
}

gen_svg logo-bulrush \
  "Bulrush cattail marsh reeds: three tall slender vertical stalks with narrow pointed blade leaves rising from a common base, one stalk topped with a slim cattail seed head. Minimal flat single-color botanical line mark for a software studio logo." \
  "Flat monochrome icon, even medium line weight, no fill gradients. Draw entirely inside the viewBox with comfortable padding; do not extend past the canvas edges." &

gen_image thumb-local-first \
  "Minimal flat editorial illustration of an abstract flowchart: a few rounded rectangle nodes connected by clean right-angle connector lines, drawn as thin dark green line art on a warm cream background. Geometric, calm, generous negative space, no text, no lettering." \
  512 512 &

gen_image thumb-cli \
  "Minimal flat illustration of a command line terminal prompt: a bright green chevron and underscore cursor centered on a deep near-black background. High contrast, simple, geometric, no text or lettering beyond the prompt glyph." \
  512 512 &

gen_image thumb-sustainable \
  "Minimal flat editorial illustration of a single leaf with a slender central vein and smooth simple lobes, in soft muted sage green on a warm cream background. Calm, organic, botanical, generous negative space, no text." \
  512 512 &

wait
echo "--- all generation finished ---"
