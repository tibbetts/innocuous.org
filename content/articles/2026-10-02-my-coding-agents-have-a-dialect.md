---
title: "My Coding Agents Have a Dialect"
date: 2026-10-02
slug: "my-coding-agents-have-a-dialect"
summary: "Coding agents have favorite words. I pointed a lab of AI research agents at them: the terms are consistent, family-specific, carry real information, and no human uses them. Plus what that means for pipelines where one model checks another."
categories:
  - "Technology"
  - "computer science"
  - "AI"
---

In August, GPT said "architectural seam" in a session I was working in. I hadn't seen that phrase before, and I happened to be in a good position to find out where it came from, because I had spent the previous month pointing a group of AI research agents at exactly this kind of question. By the end of the afternoon, one agent had found the phrase in the lab's own session logs and another had reproduced it in a controlled test. The answer turned out to be more interesting than "the model likes that word."

If you use coding agents, you have noticed that they have favorite words. Claude in particular loves "seam." A group chat I'm in has names for this: "Claudese," and less kindly, "sloplingo." The working theory in that chat, and I suspect on most of Hacker News, is that these are tics. Stochastic filler.

I wanted to know whether that's true, and it mostly isn't.

## A tic or a meaningful word?

The distinction matters. A tic you can mock or ignore. A word you should learn, or at least check what it means.

So the test is whether the model uses the term the way a speaker uses vocabulary. We showed models the same code with one defect in it, in fresh sessions with no memory, twenty times each, and counted what they called it. Then we checked the term from the other directions: give the model the term cold and ask for a definition; give it pairs of nearly identical code samples and ask which one the term applies to. My theory is that a real word survives all three checks, and a tic doesn't.

"Seam" is the funny case. It isn't a machine word at all. It's Michael Feathers, *Working Effectively with Legacy Code*, 2004: a place where you can change a program's behavior without editing it, which is what you look for when you need to get untested code under test. The engineers mocking it as AI slop were, technically, mocking Michael Feathers.

They weren't entirely wrong about Claude, though, and the full story is more interesting. In a clean test, with nothing in the prompt but the code and the word never mentioned, Claude reached for "seam" in about half of our runs on testability-refactoring code. GPT used it zero times in thirty, even though it defines the term perfectly when you ask. On that evidence, both models know the word and only Claude uses it.

Then I looked at real work. In my lab's session logs, GPT running inside Codex uses "seam" constantly: "test seam," "repository seams," "lifecycle seams." In August it used the word more often than Claude did, across well over a hundred sessions. Some of that may be the setting. Those sessions work in repositories full of plans and notes written by Claude agents, and words are infectious. But OpenAI seems to think the habit is GPT's own. The prompt Codex gives GPT-5.5 includes the line: "In particular, do not lean on words like 'seam', 'cut', or 'safe-cut' as generic explanatory filler." The same instructions tell the model not to use em dashes. The newer GPT-5.6 models I was using in August never got that line, that version only says to prefer plain language over jargon.

A better example is "signature drift," the term that started this project. It names something every programmer has seen: a function's signature changes over time, and code written against the old version quietly falls out of step. Humans have words for the result ("breaking change," "mismatch") but not for the slow divergence itself. Current Claude calls it "signature drift" as its first choice in 11 of 20 fresh sessions, defines it with the time element intact, and picks the right example out of a minimal pair 8 times out of 8. The phrase barely existed on GitHub before 2023. It now appears tens of thousands of times on GitHub, mostly in text that is visibly agent-written.

## The test that surprised me

Defining a word isn't the same as the word doing any work. So we ran one more test. We wrote short messages that were identical except for one term and handed them to a blind receiver, which had to pick which of two similar bugs the sender was describing.

With "signature drift," the receiver got it right 20 times out of 20. With the nearest human term, "signature mismatch," it was at chance: 10 out of 20. With a nonsense word, 0 out of 20, because the receiver treated the missing term as a clue too.

I want to be careful here. That's one term on one carefully validated pair of examples, with Claude as the receiver. It does not show that the whole dialect is clearer, and we tried and failed to measure that in a more realistic setting, because the task was too easy at every message length we tried. What it does show is that on this pair, the machine's phrase carried information that our vocabulary didn't.

## Nobody human speaks it

The part I find strangest is what happens on the human side. We searched everywhere we could reliably isolate a human typing. In the full history of Hacker News comments, "leaky abstraction" appears 1,991 times. The coined terms appear zero times. Stack Overflow, also zero. The vocabulary is all over GitHub, but most of the GitHub usage is visibly machine-written.

So engineers can hear the dialect well enough to make fun of it, and they still don't use it. Every technical jargon I can think of was built by people talking to each other: printers, pilots, surgeons. This one is spreading at industrial scale with no human speech community behind it at all.

The models seem to know this, for what it's worth. Asked to rate how established their own coinages are, they rate them low. Claude gives "signature drift" about 15 out of 100, which matches the historical record.

## Where does it come from?

I would love to claim the cause is reinforcement learning. I don't think we can.

What we can say is narrower. An open-weight GPT-family model whose training data predates the explosion of these terms still produces GPT's coinages, so the vocabulary travels with the model family. DeepSeek, which shares no lineage with any of the American labs, has the most transmissible terms anyway, so a family connection isn't required either. (It may have picked them up by training on other models' output. We can't tell.) And when we ran the stage checkpoints of a fully open pipeline (Allen AI's Tülu 3: fine-tuning, then preference tuning, then RL), none of the vocabulary showed up at any stage, and none of it was in any stage's training data. Our best reading is that the vocabulary is installed by what goes into post-training, not by which kind of post-training it is. That last open pipeline's RL step was trained on math problems, so it never had a chance to teach these words. The experiment that would actually settle the RL question needs stage-by-stage checkpoints from a frontier lab, and nobody publishes those.

The vocabularies also change from release to release. In one Claude line, "best-effort" (for an operation allowed to fail without failing its caller) went from the first choice in 14 of 20 runs, to 3 of 20 in the next version, then back to 17 and 20. A word lost its place for one generation and then won it back. I can't tell you why, because we can't see the training decisions, but we can date it pretty precisely.

## Same word, different meaning

Here is the part with practical consequences. The model families don't just have different words for the same bug. Sometimes they have the same word for different bugs.

"Asymmetric setup/teardown" is a Claude-family term. To Claude it means teardown that releases fewer resources than setup acquired. Gemini knows the phrase, rates it as widely recognized, and uses it to mean setup and teardown that happen in different places. Each model is consistent. They disagree with each other.

This is the biscuit problem. An American and a Briton both say "biscuit," both are sure what it means, and they find out they disagree when the plate arrives. When we had models from different families describe bugs to each other in 15-word messages, the false friends caused no mistakes at all, because the senders described what they meant. The risk is in short labels: a verdict field, a "pattern: asymmetric setup/teardown" line in a review template, a pipeline that counts two models naming the same pattern as agreement.

One of our own early results seemed to show the families agreeing on what these words meant. Then we ran a check: we gave each model a definition that had been rewritten to clearly fit a piece of code, and asked whether the term applied. Two of the three models kept saying no, sometimes while agreeing in their own explanation that the definition fit. Their agreement wasn't telling us anything about meaning, so we stopped using that test.

So, if you run a pipeline where one model checks another's work:

- Don't treat agreement on a term as agreement on a finding. Have each side define the term and give an example before you count the match. It's cheap.
- Watch the short fields. The terser the channel, the more a shared word can hide.
- If your reviewer uses a term you don't recognize, ask for a definition before you act on it. It's probably a real distinction. It may not be established vocabulary, and it may not mean what the other model thinks it means.

## How this got done

I should be clear about who did what. I ran this as a lab of AI research agents. I picked questions, approved budgets, and made the calls when an agent and I disagreed about what a result meant. The agents designed the experiments, wrote down their predictions before running anything, spent about $33 on API calls, and did the analysis. Every claim went into a ledger that caps how strongly it can be worded, which is why this post says the models "converged on" these terms and never that they "invented" them. For several terms there's a distant human ancestor if you dig hard enough.

We also looked inside a model. Claude and GPT can't be opened up, but Llama can, and [NDIF](https://ndif.us/), an NSF-funded service run out of [David Bau's lab](https://baulab.info/) at Northeastern, lets researchers run code inside large open models without owning any GPUs. When we erased the word "drift" from Llama's internal representation of a sentence, its sense of "gradual change over time" went with it, and when we transplanted that representation into a nonsense phrase, the meaning followed. I'll write that up separately.
