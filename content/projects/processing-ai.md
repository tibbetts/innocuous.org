---
title: "Processing AI"
date: 2026-08-19
summary: "Describe a generative sketch in a sentence; Claude writes the p5.js and it runs live in a sandboxed canvas you can save, remix, and embed."
site: "https://processing.bulrushlabs.com"
stack:
  - Next.js
  - TypeScript
  - Postgres
  - p5.js
  - Claude API
---

*"A flock of particles that scatter when the mouse gets close, in dusk
colours."* Processing AI turns that into working [p5.js](https://p5js.org/)
and runs it immediately in the browser. If it throws, the error goes back to
Claude with the code and comes back fixed. If you like it, save it; if you like
someone else's, remix it or mash two sketches together and see what falls out.
It's live at
[processing.bulrushlabs.com](https://processing.bulrushlabs.com).

The lineage here is Processing and openFrameworks — creative coding as a way to
think with a computer rather than a way to ship software. What natural language
changes is the cost of the first attempt. The gap between having an idea and
seeing it move used to be an hour of API-reference reading; now it's a
sentence, and you spend the hour on the fifth variation instead of the first.

## What's in it

Generation with AI-suggested prompts for when you're stuck, live preview with
playback controls, and error-fixing that reads the actual exception. Around
that, the social layer that makes a gallery worth having: search, sorting,
featured work, thumbnails, likes, threaded comments, tags, follows, and
notifications. Sketches carry version history, so a remix knows what it came
from. Anything can be embedded elsewhere with an OpenGraph card.

## Running a stranger's generated code in your browser

Every sketch is code the visitor didn't write, produced by a model, executing
in their session — so the interesting engineering is the blast radius. Sketches
run inside an iframe with `sandbox="allow-scripts"` and no `allow-same-origin`,
which puts them in an opaque origin with no reach into the page, its cookies,
or its storage. The parent talks to the sandbox purely over `postMessage`, and
because an opaque origin can't be validated by name, inbound messages are
matched against the iframe's own window reference rather than a string
comparison on `event.origin` that would be trivially satisfied.

## Somebody has to pay for the tokens

Every generation costs money on somebody's account, so the app is explicit
about whose. Bring your own key and it's yours: the key lives only in the
browser's `localStorage` and rides along as a request header, never written to
the database, never logged, never persisted server-side. An Anthropic API key
is a live billing credential, and storing other people's would turn any
database breach from "user records leaked" into a credential disclosure with a
revocation deadline attached. The cost of that choice is that your key doesn't
follow you between browsers, which is the right trade.

Requests billed to the shared key meet two ceilings: a per-user daily cap so
one account can't eat the whole budget, and a global daily cap so a traffic
spike degrades into "come back tomorrow" rather than an invoice. Both counters
increment inside a single transaction and the totals are checked *after* the
write — exceeding either throws and rolls the transaction back, so a rejected
request never consumes quota. Reading, deciding, then writing is the version
where two concurrent requests both pass a check against the same stale count.

Separately, the per-route rate limits — generation, error-fixing and mashups
each get their own window, since they have different costs and different abuse
shapes — fall back to an in-memory map when Redis isn't configured. That's fine
locally and quietly wrong in serverless, where every instance keeps its own
map. It's noted in the code as the caveat it is rather than left as a surprise.
