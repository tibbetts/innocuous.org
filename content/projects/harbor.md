---
title: "Harbor"
date: 2024-05-20
featured: true
summary: "Local-first task and project management for dev teams."
repo: "https://github.com/tibbetts/harbor"
stack:
  - TypeScript
  - Electron
  - SQLite
  - React
highlights:
  - "Offline-first by design"
  - "Markdown notes & linking"
  - "Git-friendly sync"
  - "Fast, minimal, reliable"
---

Harbor keeps your tasks, notes, and projects on your own machine. It syncs
through Git when you want it to, and works exactly the same when you are
offline.

## Why local-first

Most task managers assume a live connection to someone else's server. Harbor
inverts that: the local SQLite database is the source of truth, and sync is a
background convenience rather than a precondition for opening the app.
