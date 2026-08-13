---
title: "Analysis of May 6th: The Importance of Near Misses"
date: 2010-06-27T23:05:00
slug: "analysis-of-may-6th-the-importance-of-near-misses"
wp_id: 70
categories:
  - "Technology"
tags:
  - "engineering"
  - "finance"
source_capture: "pages/articles/2010/06/27/analysis-of-may-6th-the-importance-of-near-misses/index.html"
---
Since writing about [stock market crashes and normal accidents](http://innocuous.org/articles/2010/06/14/normal-accidents-and-stock-market-crashes/), I spent even more time talking about the events of May 6th. Good analysis is starting to come out. The best I have seen so far is [Nanex’s Flash Crash Analysis](http://www.nanex.net/20100506/FlashCrashAnalysis_Intro.html). Their conclusion is that the crash was precipitated primarily by a queuing and timestamping bug at NYSE, which lead to understandable but unfortunate flash mobbing by high frequency trading firms attempting to execute against the delayed prices being quoted out. I recommend their analysis and the supporting charts, which are quite compelling.

Nanex makes [a few concrete suggestions](http://www.nanex.net/20100506/FlashCrashAnalysis_CompleteText.html): NYSE should fix their timestamping logic, HFT firms should be discouraged from what they call “quote stuffing”, and quotes should have a minimum time to live of 50 milliseconds. The last suggestion is the most interesting, and would have a significant impact on market dynamics, but possibly not a significant impact on prices or the availability of liquidity. Many other markets (Brazilian equities, US futures) have some kind of charge for canceling or modifying orders. This kind of restriction or discrimination doesn’t prevent high frequency traders from operating, but it does change their strategies, and it might help to discourage runaway markets.

What I have found myself recommending, rather than these changes to address the immediate problem, is a need for cultural change, to identify potential future system accidents and resolve them before they make headlines. In [part 2 of the Nanex report](http://www.nanex.net/20100506/FlashCrashAnalysis_Part2-1.html), they identify two previous days on which a similar delay in NYSE quotes occurred without triggering a run on the market. With 20-20 hindsight, one might guess that investigations of these previous events would have been sufficient to prevent or limit the damage on May 6th.

Unfortunately, the culture of American capital markets is hyper-competitive, and that’s something our governments has encouraged through deregulation. Market operators are in competition with one another, brokers are in competition, trading firms (HFT and otherwise) are in competition. A culture of secrecy, and of exploiting weaknesses, makes investigating anomalous market events and other bugs very difficult. Technological transparency is important for the health of the whole financial system, but firms aren’t yet ready for it.

Short of distasteful regulatory enforcement, it’s hard to see how we would get people to participate in any kind of information sharing. But if we want to avoid future instances of market, we’ll need to find a way. There are always going to be bugs in the software we use to operate our financial system. The question is whether we find them among friends, or if we wait for the bugs to make headlines.
