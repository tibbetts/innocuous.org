---
title: "Reading Leveler"
date: 2026-08-18
summary: "Adapt any classroom reading in under a minute — one passage, three reading levels, with the concepts kept intact."
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
science reading by hand, three times. Reading Leveler does
that in about a minute.

Just paste in a passage, and Reading Leveler produces three versions — **Support** (grades 2–3),
**Core** (grades 4–6), and **Extension** (grades 7–8) — with inline change
markup so you can see exactly what moved, per-paragraph refinement when one
paragraph lands wrong, and printed handout support. It's live at [reading.bulrushlabs.com](https://reading.bulrushlabs.com).

## Adaptation rather than simplification

"Rewrite this more simply" is a solved prompt. What teachers actually
need is an accessible reading where the *educational* content
survives. The student still has to get the key concepts, causality, chronology, factual and scientific accuracy,
and the academic vocabulary the unit is teaching. A Support version of the
photosynthesis reading that no longer contains the word *chlorophyll* has
removed the lesson.

Reading Leveler has specific support for protected terms. The AI is told which vocabulary must
survive the rewrite, and the readability scorer excludes those terms and proper
nouns. Otherwise "Declaration of Independence" alone drags the grade estimate
up and the tool starts stripping out the very words the reading exists to
teach.

## Hitting a grade level is an engineering problem

Flesch–Kincaid is `0.39·ASL + 11.8·ASW − 15.59` — average sentence length and
average syllables per word. Protected vocabulary and named entities push
syllables-per-word to roughly 1.35 in real classroom passages rather than the
1.28 you'd assume, which changes the sentence lengths you have to aim for. The
prompts are tuned for that: Extension
needs about 18-word sentences to reliably reach grade 7.5, while 15-word
sentences only get to 5.5. Each level also carries a max-sentence cap, otherwise
a single 30-word sentence could hide behind a good average, and it is
precisely the sentence a struggling reader stalls on.

When a level lands outside its band the app retries with the miss fed back in —
but only when the miss is larger than half a grade. That threshold came out of
the eval harness: asked to make a small adjustment from a near miss, Anthropic Sonnet 4.6
reliably overshoots by two or more grades. A retry that makes the result worse
is worse than no retry, so near misses are left alone and surfaced to the
teacher instead.

Prompt changes are evaluated offline against a fixed corpus of science and history
passages before they reach production.

## How can I use it?

Reading Leveler is in private beta, but the demo is open and doesn’t require a login. If it looks useful for your classroom and you want an account for saving passages and trying the full workflow, send me a note. I’m especially interested in feedback from teachers using it on real material.
