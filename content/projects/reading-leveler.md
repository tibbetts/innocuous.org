---
title: "Reading Leveler"
date: 2026-08-18
summary: "Differentiate any classroom reading in under a minute — one passage, three reading levels, with the concepts kept intact."
site: "https://reading.bulrushlabs.com"
stack:
  - Next.js
  - TypeScript
  - Supabase
  - Clerk
  - Claude API
---

A fifth-grade teacher may be running one lesson across students reading at a
second-grade level, on-level readers, advanced readers, English language
learners, and students with accommodations. The usual answer is to rewrite the
science reading by hand, three times, on a prep period. Reading Leveler does
that in about a minute.

Paste a passage, and it produces three versions — **Support** (grades 2–3),
**Core** (grades 4–6), and **Extension** (grades 7–8) — with inline change
markup so you can see exactly what moved, per-paragraph refinement when one
paragraph lands wrong, and a copy or print of whichever level you're handing
out. It's live at [reading.bulrushlabs.com](https://reading.bulrushlabs.com).

## Not simplification — differentiation

The design constraint that makes this hard is that the easy version of the
problem is the wrong one. "Rewrite this more simply" is a solved prompt. What
teachers actually need is complexity reduced while the *educational* content
survives: key concepts, causality, chronology, factual and scientific accuracy,
and the academic vocabulary the unit is teaching. A Support version of the
photosynthesis reading that no longer contains the word *chlorophyll* has
removed the lesson.

So protected terms are first-class. The model is told which vocabulary must
survive the rewrite, and the readability scorer excludes those terms and proper
nouns — otherwise "Declaration of Independence" alone drags the grade estimate
up and the tool starts stripping out the very words the reading exists to
teach.

## Hitting a grade level is an engineering problem

Flesch–Kincaid is `0.39·ASL + 11.8·ASW − 15.59` — average sentence length and
average syllables per word. Protected vocabulary and named entities push
syllables-per-word to roughly 1.35 in real classroom passages rather than the
1.28 you'd assume, which changes the sentence lengths you have to aim for. The
targets are tuned against that measured number, not the ideal one: Extension
needs about 18-word sentences to reliably reach grade 7.5, where 15-word
sentences only get to 5.5. Each level also carries a max-sentence cap, because
a single 30-word sentence hides comfortably inside a good average and is
precisely the sentence a struggling reader stalls on.

When a level lands outside its band the app retries with the miss fed back in —
but only when the miss is larger than half a grade. That threshold came out of
the eval harness: asked to make a small adjustment from a near miss, Sonnet
reliably overshoots by two or more grades. A retry that makes the output worse
is worse than no retry, so near misses are left alone and surfaced to the
teacher instead.

Prompt changes are A/B'd offline against a fixed corpus of science and history
passages before they reach production, with runs kept as JSONL so a regression
is a diff rather than an argument.

## What it taught me about shipping

Three bugs found in one audit session shared a shape worth naming: every status
field was honest about the thing it described and silent about the thing that
was broken. A link-preview image endpoint had 404'd for six weeks while the app
itself returned 200. Production telemetry was being written with `console.log`
on a plan that retains runtime logs for one hour — six weeks of "wait for data
before building the next layer" was gated on data that never survived the hour
it was written in. And a health check asserting "this route isn't 404" passed
against a build that had the exact bug it was meant to catch.

That last one produced the rule I now apply everywhere: **a negative test needs
a fixture that can actually express the failure.** I'd reached for the old
deployment that *had* the bug, but it sat behind deployment protection and
answered 401 before the app was ever reached — so the check passed via an auth
wall unrelated to what was being tested. The fix was to point the detector at a
route that is *supposed* to fail that way permanently, by design. It's stable,
it's live, and it can't drift out of reproducing the condition.
