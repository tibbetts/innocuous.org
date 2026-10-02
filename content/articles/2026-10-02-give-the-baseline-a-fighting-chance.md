---
title: "Give the Baseline a Fighting Chance"
date: 2026-10-02
slug: "give-the-baseline-a-fighting-chance"
summary: "When your research system beats an LLM baseline, check that the baseline got real effort. How to build a strong alternative: make one example work, investigate surprises, spend enough to see stability, and find the work that is still yours."
categories:
  - "Technology"
  - "computer science"
  - "AI"
---

I’ve been working with Fabian Wenz and MIT database researchers on [Rubicon](https://arxiv.org/abs/2604.21413v3), trying to make AI useful for working with data while preserving repeatability, accuracy, and inspectable results. My old advisor Mike Stonebraker connected me with the project. Much of my recent guidance to Fabian has been about evals, benchmarks, and how to steelman the alternative.

The difficulty is that finding out what a capable model can actually do takes work. You have spent months on your research system. Then you pick a model, write a prompt, and call that the baseline. It does badly. Your system does well. This is a very convenient result.

I remember back in 2007 when everyone seemed to be beating Hadoop by a factor of two or five. Of course they could. They had optimized their own system and barely touched the Hadoop deployment.

The lesson I took from Stonebraker back then was to aim for 50 or 100 times better in research. After commercialization, realistic workloads, and comparison with a properly tuned incumbent, you might retain a factor of ten. And ten was roughly what you needed to persuade an industrial customer to try an edgy new system.

What “100 times better” means for LLMs is outside today’s scope. But the lesson about giving the baseline appropriate attention still applies. To find out whether your system beats what someone could reasonably use today, give it a strong, well-configured alternative. Here are some suggestions for how to do that with LLMs.

## Make one example work

Before running a large benchmark, work through one case interactively in Claude Code, Codex, or whatever gives the model appropriate tools. Let it write SQL or Python when computation would help. Point it toward the documentation. Show it an example of a useful answer. Find out whether you can get it to do the work.

If you cannot walk it through the task, revisit your own understanding too. Can you explain the steps and recognize a good answer? This can feel like helping a toddler, but it is worth finding out where things break down. If you can’t walk the model through even one instance of the task end to end, there might be something impossible in your task. Generally I find people can get it done.

Then ask it to write down the procedure as a skill or prompt. Try that in a fresh session, without your help, and on other test cases. Along the way make sure your test scripts can display transcripts, export a case for interactive use, and grade a manually executed case. Investigating one failure should be easier than running another hundred examples.

## Investigate surprising results

A useful benchmark should probably distinguish different classes of models. I would expect a smarter model, or a larger thinking budget, to help. If it doesn’t, find out why. Perhaps the questions are too easy, too hard, or mostly measuring a tooling bottleneck.

One frontier model we tried appeared to have the relevant US Department of Transportation rules memorized, including page numbers. Unfortunately, it had the wrong edition memorized. It seemed to trust what it knew instead of looking at the supplied sources. That explains how knowing more could make it do worse.

It also suggests a fix: require the model to find support in the specified edition, then check whether it does. If better prompting solves the problem, that improves the baseline. We should not preserve a fixable mistake because it makes our system look better.

Always save the whole transcript, including tool calls and results, along with the configuration and source versions. Read failures and successes. A passing score can hide a broken grader. If there is one thing I learned at Anthropic it is to read transcripts of your evals.

Consider a reference answer saying a longer green light would delay buses too much on a particular street. The model says it would affect public transit. Is that wrong? It depends on whether the task needed a broad reason or an explanation useful to a resident. Write down which details matter.

And when someone says the model never gets the JSON wrong, or some other answer format detail, check where invalid responses go. Are they repaired, retried, or silently dropped?

## Spend enough to understand the result

Start with three runs. If results are unstable, try ten and investigate what changes. These are practical starting points, not statistical guarantees; similar averages can conceal different questions failing. The important thing is to run enough examples of the same case to see stability. If you don’t have stability, you’ll need to figure out what to change to get it.

At $20 a run, three runs cost $60. A hundred cost $2,000, so there is a budget question. But I would rather spend $60 than build a research direction around a lucky $20 result. Use cheaper models during development, or even cache model responses to speed things up and save API credits to spend when you are getting useful data.

Measure restrictions too. In our BEAVER test runs, a ten-minute timeout interacted with an API rate limit. Eighteen attempts hit the cap. Some even scored as correct because both the prediction and reference results were empty. That kind of thing can mask errors, and is another reason to read transcripts, even successful transcripts. It’s also a case where you might see less capable, faster models score differently. Investigate all the anomalies.

## Find the work that is still yours

Of course you can make a benchmark succeed by fixing the prompt for every case. Hopefully you have plenty of held-out cases. Develop and compare prompts separately from the final test set. Once a test failure informs a prompt change, that case is no longer valid for real testing.

But suppose the procedure works on fresh cases and producing it took substantial expertise. You can look at the prompt and decide your research contribution is that it should not be this hard.

Try prompt ablation: remove examples, source-selection instructions, or checking steps and measure the effect. For a long prompt, remove groups and narrow down the important parts, perhaps in something like a binary search. Instructions interact, so follow up on those candidates with controlled comparisons. Use repeated runs on development or validation cases; preserve the final test set.

Learning which instructions matter, how much they help, and whether they transfer can be useful research itself. So can building a system that saves users from having to discover those instructions repeatedly.

Take a question your baseline gets wrong. Work through it, capture what helped, and try again on fresh cases without your intervention. You may lose a convenient result. You will have a much better idea of what to work on.
