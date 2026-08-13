---
title: "DEBS 2010 Highlights"
date: 2010-07-18T22:49:00
slug: "debs-2010-highlights"
wp_id: 73
categories:
  - "Technology"
tags:
  - "computer science"
  - "event processing"
source_capture: "pages/page/2/index.html"
---
I spent the first half of last week at [DEBS 2010](http://debs10.doc.ic.ac.uk/) at King’s College in Cambridge, UK. It was a great conference, many good papers and interesting attendees. As usual some of the best ideas came from the hallway sessions. But I’d like to provide some pointers to my favorite papers of the conference:

- David Jeffery’s [keynote](https://portal.acm.org/citation.cfm?id=1827418.1827447&coll=portal&dl=GUIDE) on Betfair’s event driven architecture, past present and future. David presented not only on the performance challenges of running the core betting exchange, but also on the soft benefits. Thanks to their event driven architecture, Betfair is able to do more experimentation with less disruption, and be more agile as an organization.
- Dan O’Keeffe presented [Reliable Complex Event Detection for Pervasive Computing](https://portal.acm.org/citation.cfm?id=1827418.1827429&coll=portal&dl=GUIDE), a system for compensating for missing data. Most importantly, it lays out a selection of strategies that developers can select and the system can use to automatically choose the correct approach, based on wether the system should be optimistic, pessimistic, or something in between.
- [Quilt: A Patchwork of Multicast Regions](http://www.cs.cornell.edu/projects/quicksilver/public_pdfs/DEBS-CRC.pdf) was presented by one of the local students on short notice, because the author was not able to attend due to visa problems. This is especially frustrating when the paper is so interesting and the analysis quite strong. Quilt is a system for combining multiple delivery mechanisms to achieve efficient wide area distribution. Combining overlay-network based protocols with “patches” of true multicast where available, Quilt optimizes message routing for efficiency, reliability, and latency.
- [An Approach for Iterative Event Pattern Recommendation](https://portal.acm.org/citation.cfm?id=1827418.1827459&coll=portal&dl=GUIDE) which was also presented by a colleague rather than one of the authors due to visa issues. The paper describes a system for recommending event patterns to domain experts based on their initial attempts to define the pattern. In a controlled user study, the recommendation system substantially reduced the time taken by users to define novel patterns. It was good to see a real user study of a programming efficiency system, but there is lots of room for further measurement.
- [Experiences with Codifying Event Processing Function Patterns](https://portal.acm.org/citation.cfm?id=1827418.1827460&coll=portal&dl=GUIDE), presented by the author Anand Ranganathan, dealt with a different kind of pattern. In systems using Ranganathan’s system, developers build template network flows, annotated with tags to define what components can be used in the flow. Any component that matches the inputs, outputs, and tags can be inserted into the template, and all possible template instantiations represent a domain of valid applications. End users are able to search this combinatorially large domain with a flexible interface, to find and instantiate applications that meet their needs.

There are many great papers and talks not listed here. Obviously my own bias shows, as does the fact that I didn’t attend every talk or read every paper.

Unfortunately most of the links go to the ACM portal, which doesn’t offer public access. My frustration with and thoughts on the future of academic publishing will have to wait for a future post. I recommend googling the titles and finding them on author pages if you can. Or ping me and I can send you papers.

Next year the conference will be hosted in New York by IBM research. Whether you attended or not, if you have any feedback on how to make the conference more appealing, I’m happy to hear it.
