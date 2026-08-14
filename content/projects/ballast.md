---
title: "Ballast"
date: 2026-08-05
featured: false
summary: "A conservative reviewer for Postgres migrations, built for teams whose SQL is increasingly written by AI."
repo: "https://github.com/tibbetts/ballast"
stack:
  - Postgres
  - Python
  - Node
  - Claude Code
highlights:
  - "Blocks destructive DDL and supplies the safe rewrite"
  - "Machine-parseable verdicts you can gate CI on"
  - "Eval-driven: every claim has a findings doc"
  - "Ships as one Markdown file"
---

*Ballast keeps the ship from capsizing — and your established schema is the
ballast every new migration loads against.*

Ballast reviews Postgres migrations before they run. It exists because the
migrations arriving in code review are increasingly not written by people, and
the failure modes of machine-written DDL are specific enough to be worth a
specific guard.

The deliverable is deliberately small: **one Markdown file**, a review skill
that blocks destructive DDL with the safe rewrite supplied, flags lock-window
and idempotency hazards, and approves clean changes without manufactured
caution. You get a verdict in YAML front matter — `approve`, `caution`, or
`block` — which means you can grep it in CI, a short rationale naming the
specific concern, and corrected SQL when something is wrong.

## What it catches

**Verdict-downgrading**, which is the measured number-one failure mode of
frontier models on real migrations: the model names the data loss in its own
rationale and then approves the migration "conditionally." Ballast's
anti-downgrade rule holds at ceiling across Django, Diesel, Rails, Laravel and
Prisma fixtures, including adversarial cases where the file is named
`_safe.sql` and contains a `DROP` (20/20 correct blocks).

**Availability traps** — `CREATE INDEX` without `CONCURRENTLY` on a large
table, `NOT NULL DEFAULT now()` full-table rewrites, foreign keys added without
`NOT VALID` — each with the multi-step safe rewrite suggested.

**Semantic bugs that no regex linter fires on.** During validation the skill
overruled its own exercises' answer keys twice, and was right both times: a
self-recursive RLS policy that would recurse infinitely on the first real
query, and a nondeterministic `UPDATE ... FROM` backfill locked in by a
following `NOT NULL`. Both reproduce on Sonnet, Opus and GPT-5.

It complements deterministic linters like `strong_migrations` or `squawk`
rather than replacing them. Those check syntax against rules; this is the
judgment layer that reads intent and proposes a rewrite.

## Measured, not asserted

The project's organising discipline is that no claim ships without a findings
document and the run data behind it. Across a 41-migration deployment corpus
spanning three projects and three migration tools, verdict match with project
context runs 35–36 of 41 on Claude models and 32 of 41 on GPT-5, with
destructive and availability recall at 12/12 in every arm.

The most instructive number was a bad one. GPT-5 initially scored 63%, and the
gap turned out to have two independent causes, each individually sufficient:
the harness was not passing project instructions the way Claude Code does, and
the framework-exemption prose needed an explicit conditional gate. Passing
project context alone is worth about 17 points on GPT-5 — enough that it
became a design constraint on the forthcoming MCP server.

The cleanest external evidence comes from a probe against 42 real migrations
from `mastodon/mastodon` with no context supplied. Ballast approved 83% of the
clean sample silently, blocked the one real `TRUNCATE`, and correctly ignored
`remove_column` verbs that appear only in `down()` methods. Its two headline
flags are validated by Mastodon's own history: the 2017 non-concurrent
`notifications` index it blocked is precisely the index Mastodon rebuilt with
`CONCURRENTLY` three months later.

Known limitations are documented with the same care as the wins: a
conservatism bias on borderline lock-window cases, a dependence on stated table
sizes for tables the model does not know, per-model-version drift on borderline
verdicts, and circularity caveats on the LLM-authored exercises — which is why
the bug catches and the Mastodon probe are treated as the uncontaminated
evidence.

## The research behind it

Ballast came out of a roughly two-month eval-driven research programme run
under the codename **GuardedDB**: controlled arms, LLM-judge scoring,
pre-registered predictions, and negative results kept rather than quietly
dropped. That programme is where the skill is developed and evaluated; this
repository carries the releases.

A paper on the work was submitted to **CIDR 2027**.

## Installing

Ballast ships as a Claude Code plugin, a pip package, or a file you copy:

```
/plugin marketplace add tibbetts/ballast
/plugin install ballast@ballast
```

```bash
pip install ballast-db
ballast install-skill ~/code/your-project
```

Then ask *"review this migration — is it safe to apply?"*.

One line per large table in your `CLAUDE.md` (`events` has ≥10M rows) makes the
lock-window rules fire reliably. Without stated sizes the skill prefers
`caution` over guessing, which is the correct bias but a noisier one.
