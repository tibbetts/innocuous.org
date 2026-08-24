---
title: "Clawhammer"
date: 2026-08-23
summary: "Agentic window layout for macOS: tell Claude how you want your screens arranged and it sorts them out — per-screen roles, packed layouts, and a way to find what you should just close."
repo: "https://github.com/tibbetts/clawhammer"
stack:
  - Lua
  - Hammerspoon
  - macOS
  - Claude Code
---

I have a lot of screen real estate, and more of it since I added a very large
widescreen monitor. It turns out that having somewhere to put everything is not
the same as things being in the right place. Windows drift, pile up behind each
other, and land on whichever display they were last opened on; by the middle of
a working day it's all thoroughly cluttered, and tidying it by hand is dull
enough that I don't.

So I wanted Claude to be able to help. Clawhammer is the result — a Hammerspoon
config you talk to, which gives each screen a role and arranges your windows
into it.

You say *lay out my screens* and it does: browsers left, terminal centred, chat
on the panel above, monitoring on the other one. Displays are addressed by
**role** rather than by name, so the layout survives replugging a monitor, a
Screen Sharing session collapsing everything onto one virtual display, or an
app relaunching after a crash and scattering its windows.

## When no arrangement helps

Some days the clutter isn't a layout problem, and it took measuring to believe
it. Thirty-nine windows on a 7680×2130 ultrawide came to **52.5M px² of window
area on a 16.4M px² screen — 3.21×**. At that density no
arrangement can show everything while sizes are preserved. The best possible
zero-overlap packing fit **14 of 39**, and only by favouring the *smallest*
windows, which are the least important ones.

So the honest answer wasn't a cleverer algorithm. It was: close some windows.

That turned out to need evidence rather than nerve, which is where the other
half of the tool came from. Clawhammer samples which window has focus every few
seconds and keeps a timeline. Cross-referencing that against what's currently
open produces a close list ranked by how long since you last actually touched
each window — in one real session, nine windows had never been focused at all
while tracking ran, alongside a Contacts window untouched for 38 days and a
`localhost` error page for 36. Closing everything older than a week took the
same screen from 3.21× to 2.11×; older than three days, to 1.49×. Below about
1.0× the packer reaches genuine zero overlap, and the whole problem dissolves.

Which means the tool's most useful answer is sometimes "stop arranging, start
closing" — not what I set out to build, but the one the numbers supported.

## Sizes belong to you

Most tilers resize your windows. Clawhammer's default is that the size you
chose is yours: when things don't fit it spaces them out or cascades them
rather than shrinking them silently. How far that goes is a setting, not a
principle — `never`, `tile` (the default, where commands that divide a screen
into zones may resize into them), or `always`.

There's a related rule about what to optimise. Overlap area turns out to be the
wrong metric: a window 90% covered but with a clear title bar is one click from
the front, while a buried one is lost. So the built-in scorer measures
**title-bar visibility against real z-order**, and that's what layouts are
compared on.

## Nothing is on until you ask

A fresh install does nothing. No focus tracking, no browser-history reading, no
hotkeys — a tool that starts recording your activity or claims five system-wide
chords the moment it's installed has helped itself to things it was never
given.

Focus tracking is the sharp end of that. Window titles are not innocuous: an
audit of one real 48-day log found, among 1,430 distinct titles, 152 email
subject lines, 82 named individuals, 34 legal or confidential documents, 17
financial and 8 medical. Everything useful about time tracking survives without
them, so **titles are redacted by default** and full capture is an explicit
opt-in that says plainly what will be written to disk.

## Why this is harder than it looks

macOS fights you in specific, non-obvious ways, and the skill that ships with
the plugin is largely a catalogue of them:

- **`hs -c "hs.reload()"` deadlocks.** Reloading tears down the IPC port before
  the reply is sent, so the client blocks forever — and the stuck clients then
  jam the port for every later call. The symptom is baffling: even
  `hs -c "return 1+1"` hangs while Hammerspoon sits at 0% CPU looking perfectly
  healthy, which sends you hunting for an infinite loop in your own code.
- **`mainScreen()` follows the focused window**, so anchoring a screen role to
  it means the role silently moves when you click elsewhere.
- **`moveToScreen`'s second argument is `noResize`.** Get it backwards and
  macOS *scales* every window moving between displays of different widths.
- **You cannot control cross-application z-order.** It follows app activation,
  so a cascade whose readability depends on a global front-to-back order simply
  will not work. Measured ceiling for raising windows in order: 29% → 32%
  title visibility.
- **App names carry invisible characters.** WhatsApp reports its name with a
  leading U+200E left-to-right mark, so a plainly typed `"WhatsApp"` rule never
  matches anything.

Each of those cost an afternoon. They're written down so they cost you nothing.

## Testing something that moves your windows

The obvious way to test a window manager is to let it rearrange your desk and
look at the result. That's slow, disruptive, and tests exactly one
configuration — the author's.

So the layout engine is pure where it matters: every module exposes a
`plan(items, frame, opts)` that takes plain tables and returns placements, and
a single small module is the only code that touches a window. A five-screen
desk, a laptop with one display, or a policy of never resizing are all
fixtures, and the whole suite runs on Linux in CI in milliseconds.

That refactor paid immediately. A single-display test caught a bug three
monitors never would: roles were assigned in sorted order, and on one display
every role degrades onto the same screen, so a laptop resolved its only screen
to "comms" and never to "work". CI also greps for personal detail on every
push — a clean credential scan tells you nothing about whether a real hostname
or window title has been committed, and that's the check this project needed
most.

## Installing

Clawhammer ships as a Claude Code plugin:

```
/plugin marketplace add tibbetts/clawhammer
/plugin install clawhammer@clawhammer
```

Then run `/clawhammer-setup`. It installs Hammerspoon if you don't have it,
looks at your displays, and proposes which screen plays which role by inferring
it from where your windows already sit — you correct it rather than describing
your desk from scratch. It asks before reading anything about your screens and
writes nothing until you've seen the exact config. `--dry-run` walks the whole
flow and changes nothing.

After that, *"tidy up my screens"* is the whole interface. `arrange` is the
whole-desk command, and `undoLayout` puts every window back where it was.

Setup has been exercised on one three-display Mac and in fixtures — not yet on
a laptop or anyone else's machine — so expect rough edges in the questions it
asks rather than in what it does.
