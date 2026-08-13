---
title: "Algorithms for the 21st Century"
date: 2006-09-28T22:51:00
slug: "algorithms-for-the-21st-century"
wp_id: 25
categories:
  - "Technology"
tags:
  - "algorithms"
  - "computer science"
  - "math"
  - "programming"
source_capture: "pages/articles/2006/09/28/algorithms-for-the-21st-century/index.html"
---
Went to a talk at MIT tonight, by [Stephen C Johnson](http://yaccman.com/), a researcher at [The Mathworks](https://www.mathworks.com/). The talk was sponsored by the [Greater Boston ACM](http://www.gbcacm.org/website/semInfo.php?id=1115). The paper, [Algorithms for the 21st Century](http://yaccman.com/papers/a21/Alg21.html), was presented at Usenix 2006. The general thrust was how computer architecture has drifted from the idealized model used in most algorithms classes, in significant ways. The major focus was on the memory subsystem, and how caching can effect algorithmic performance. By looking at the behavior of very simple algorithms, we can see fairly complex variations in performance, by factors as high as 60 times worse. This in turn implies that the performance of complex algorithms will be even more diffi  
cult to characterize.  
One big take-away is that the built-in cache management schemes of modern memory systems are pessimal for certain algorithms. This actually sounds quite a bit like the complaints against operating system disk buffer/virtual memory management by database authors. Database algorithms, because they often have large storage access requirements that can be characterized in advance, benefit from managing their own buffers. Similarly, it seems like scientific computing (eg, Matlab), which wants to manipulate gigabytes of memory in very structured ways, would benefit from direct management of caching. Of course, cache management needs to run at processor-speed, unlike disk buffer management, so writing heavyweight algorithms is inappropriate. Unfortunately, the talk did not discuss any recommendations for extentions to enable management. I wonder if something as simple as being able to mark a page as no-cache in the TLB would be sufficient.  
My other take-away is that computer science researchers don’t understand computers nearly enough. The presenter, while familiar with processor design and memory architecture, wasn’t really able to explain the behavior of these simple algorithms in their entirety. I’m always bothered when I encounter this lack of understanding. On some level it seems that it should be possible to fully understand computer systems. After all, they are developed by humans, and to a first approximation their behavior is deterministic and well defined. Unfortunately, they change rapidly, and so any abstract models we develop are shortly invalidated. Fundamentally, this is what makes computer science difficult.
