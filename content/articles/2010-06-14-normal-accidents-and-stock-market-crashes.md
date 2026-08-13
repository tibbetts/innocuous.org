---
title: "Normal Accidents and Stock Market Crashes"
date: 2010-06-14T11:31:00
slug: "normal-accidents-and-stock-market-crashes"
wp_id: 69
categories:
  - "Miscellaneous"
tags:
  - "computer science"
  - "finance"
source_capture: "pages/articles/2010/06/14/normal-accidents-and-stock-market-crashes/index.html"
---
In the weeks since the precipitous and brief stock market crash on May 6th, I have found myself answering questions about it from people outside the capital markets and discussing it with insiders on many occasions. While I have some thoughts about what went on, I’m often unable to satisfy people’s desire to blame a single precipitating cause. I think what is going on is that too few people understand the nature of complex systems and what is called a “normal accident.” Given the sophistication of the markets, the number of safety checks and balances, as well as the complexity of the implementations, it is not surprising that events such as May 6th happened, nor should people think it is possible to entirely eliminate them.

Normal Accidents (or as wikipedia calls them “[System Accidents](https://en.wikipedia.org/wiki/System_accident)“) are major failures caused by unintended and unexpected interactions of many small failures. The term was coined by Yale professor [Charles Perrow](http://www.yale.edu/sociology/faculty/pages/perrow/) in his book [Normal Accidents: Living with High-Risk Technologies](https://www.amazon.com/exec/obidos/ASIN/0691004129/innocuousorg-20/ref=nosim/). Complex systems fail for complex reasons. In systems engineered for safety and redundancy the failures that do happen require many contributing factors. Perrow’s focus was on large industrial systems, such as power plants, chemical plants, aircraft, shipping, and military operations. TIme and again we see complex failures in places like Three Mile Island, the Challenger shuttle, or BP’s current oil spill.

In a normal accident, the contributing factors come from many areas and often many organizations. Errors result from poor regulation, lack of training, operator error, specification errors, mechanical failures, lax maintenance, poor morale, organizational structures, economic incentives, and many other areas. Because systems are tightly coupled, many of these factors are able to mutually reinforce one another to lead to systemic failure. The resulting cascade of failures can look like a Rube-Goldberg machine in it’s complexity.

In these tightly coupled systems, potential-normal-accidents are happening all the time. Systems are too complex to be entirely without failures. However, in the common case these partial failures are caught and resolved quietly. In fact, these near misses are an opportunity to understand the unintended failure modes of the system. Rather than build once and deploy, safety must be a continuous process of improvement and understanding. Systems aren’t stable and they are not deployed in a vacuum. As they evolve, failures and near misses must be examined and used to drive improvements.

Software, especially modern networked software, dramatically increases the incidence of normal accidents. As anyone who has ever created, deployed, and debugged software knows, it is common for individual software bugs to have all the characteristics of a normal accident all by themselves. Add together software written by multiple different organizations connecting over a network and it’s a wonder anything works at all.

Getting back to the events of May 6th, the “[Flash Crash](https://en.wikipedia.org/wiki/May_6,_2010_market_event)“, they are best explained as a system accident. People have tried to blame one cause or another, from a fat fingered trader or a faulty brokerage system, to investor agitation over Greek debt and high frequency trading firms going wild, to the NYSE hybrid market system, bugs in other members of the national market system, and outdated circuit breaker regulations. Without going into detail about all these potential causes, I’d like to suggest that the most likely explanation is that all of these causes, together, are what created the exceptional failure of market prices, broken trades, and finger pointing. No one cause is really more precipitating than any other, and apportioning blame is much less important than understanding in detail what happened.

It is impossible to eliminate normal accidents as we increase the complexity of our systems. The best we can do is to learn from accidents, and from near misses, to introduce the kind of slack in our systems that will protect us from the worst accidents. Learning requires transparency. But in systems which cross organizational and regulatory boundaries, with billions of dollars and reputations at stake, transparency is going to be a challenge.

*PS: If you’re interest in learning more, I suggest this* [*NASA powerpoint on normal accidents*](https://www.hq.nasa.gov/office/codeq/accident/accident.pdf)*.*
