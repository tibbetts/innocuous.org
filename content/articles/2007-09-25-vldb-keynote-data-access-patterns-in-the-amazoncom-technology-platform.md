---
title: "VLDB Keynote: Data Access Patterns in The Amazon.com Technology Platform"
date: 2007-09-25T06:53:00
slug: "vldb-keynote-data-access-patterns-in-the-amazoncom-technology-platform"
wp_id: 5
categories:
  - "Technology"
tags:
  - "Database"
source_capture: "pages/articles/2007/09/25/vldb-keynote-data-access-patterns-in-the-amazoncom-technology-platform/comment-page-1/index.html"
---
The opening keynote for [this year’s VLDB](http://www.vldb2007.org/) was a great presentation by [Amazon CTO Werner Vogels](http://www.vldb2007.org/program/keynotes.html#vogels), describing their data management challenges. I particularly appreciated it because it echoed something I’ve been saying for a few years now: Web-scale companies have problems which cannot be managed with standard RDBMS, or with any common research systems, and so they have started to route-around the database research community.

Vogels presented lots of information. A big part was about the operational realities of a site as large as Amazon. This has been said before, but saying it to a room full of database researchers was a good thing:

- Incremental scalability, up or down, one node at a time, is a key requirement
- Adding resources for redundancy must not hurt performance (best if it helps).
- Failures are not uncorrelated, they are generally quite correlated.
- Systems that fail do not fail stop, they generally fail in some more complex way (eg, periodically coming back up and failing again, or outputting garbage).

Amazon’s query workload shares a lot of characteristics with other web sites with which I am familiar, such as [eBay](http://www.addsimplicity.com/downloads/eBaySDForum2006-11-29.pdf), [Google](http://www.manageability.org/blog/stuff/economics-google-hardware-infrastructure/view), [Facebook](http://www.skrenta.com/2007/05/scaling_facebook_hi5_with_memc.html), and [LiveJournal](http://www.highscalability.com/livejournal-architecture). Amazon uses lots of read mostly workloads and lots of pkey-lookup-only workload (65% of all queries are primary key). Only 5% of their queries need full RDBMS query functionality. Most of their writes are also by primary key, and many storage systems support only that kind of write.

When it comes to those writes.

- Only 10% of queries need strong consistency.
- “We consider strong consistency to be evil,” because it is impossible to implement without the potential for downtime or failure.
- Most systems at Amazon are designed for eventual consistency.
- One interesting case is the need for always-writable data storage. One use case is ordering. “If the customer decides to give you his money, you must always take it, that’s a business principle.” Always writable storage obviously implies a conflict resolution scheme.

All this points to a traditional RDBMS being the wrong system. Interestingly, if you assume you need a single general purpose system, then RDBMS is the best available. But the real answer is to use a set of customized data management tools. This all echos Stonebraker’s claim that [one size no longer fits all uses](http://www.databasecolumn.com/2007/09/one-size-fits-all.html).

Where do we go from here? The real problem for the research community is not to help Amazon and Google build a 5% better system. The real problem is to package up (aka abstract) these tools in such a way that, like databases, average programmers can work with them. Because problems that PhDs at Amazon and Google solve today will soon be problems everyone needs to solve.
