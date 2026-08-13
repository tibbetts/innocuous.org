---
title: "Android G1 and Palm Pre versus iPhone and BlackBerry Benchmarks"
date: 2009-06-20T23:26:00
slug: "android-g1-and-palm-pre-versus-iphone-and-blackberry-benchmarks"
wp_id: 54
categories:
  - "Technology"
tags:
  - "apple"
  - "benchmark"
source_capture: "pages/articles/2009/06/20/android-g1-and-palm-pre-versus-iphone-and-blackberry-benchmarks/index.html"
---
In my last post, I shared [benchmark data for the web browser on the iPhone versus BlackBerry](https://innocuous.org/articles/2009/06/20/blackberry-versus-iphone-benchmarking-the-browser/). My theory is that web browser performance is critically important for smartphone user experience. Furthermore, the BlackBerry seems to be embarrassingly inferior to the iPhone in this respect. This begs the question, how do other phones stack up.

[![All Phones](https://innocuous.org/wp-content/uploads/2009/06/phones-all.png)](https://innocuous.org/wp-content/uploads/2009/06/phones-all.png)Thanks to two friends, I have SunSpider JavaScript benchmark results for the G1 and for the Palm Pre. Based on the graphs here, it’s clear that the G1 and the Pre are both considerably better than the BlackBerry Bold. Specifically, the G1 is 9.6 times faster than the Bold, and the Pre is 15 times faster.

[![All but BlackBerry](https://innocuous.org/wp-content/uploads/2009/06/phones-all-but-bb.png)](https://innocuous.org/wp-content/uploads/2009/06/phones-all-but-bb.png)On the other hand, the G1 and the Pre both compare unfavorably to the iPhone 3GS. The G1 is 6 times slower, as can be seen from the graph that excludes the BlackBerry. The Pre is 3.7 times slower. Neither the Pre nor the G1 achieve the performance of the first-gen iPhone.

Knowing the Android/G1 performance also helps to answer if this is a Java versus Objective C issue. Both the BlackBerry and Android are Java-based phone systems. Java puts a bigger burden on the virtual machine implementor to be responsible for performance, and has a reputation for overall worse performance than more native languages like Objective C. The G1 demonstrates that RIM could be doing a lot better with the BlackBerry.

it is also worth noting that the SunSpider benchmark was developed by the WebKit development team, and WebKit is the basis for the iPhone browser. It is unsurprising that the iPhone does well on this benchmark, it is likely used as part of the development process. However, it is still the best general JavaScript benchmark available.

The main conclusion to be drawn here is that if you want a web browser in your pocket, the BlackBerry is right out. When it comes to deciding between iPhone, Android, and Pre, it is likely that things other than JavaScript performance will drive your decision.
