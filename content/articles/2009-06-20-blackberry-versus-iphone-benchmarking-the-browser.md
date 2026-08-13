---
title: "BlackBerry versus iPhone – Benchmarking the Browser"
date: 2009-06-20T01:17:00
slug: "blackberry-versus-iphone-benchmarking-the-browser"
wp_id: 49
categories:
  - "Technology"
tags:
  - "benchmark"
source_capture: "pages/articles/2009/06/20/blackberry-versus-iphone-benchmarking-the-browser/comment-page-1/index.html"
---
Lately I’ve been thinking about getting a netbook. They seem trendy, and I like gadgets. But I’ve started questioning what I would get from one that I don’t get from my current devices. I’ve concluded that what I want isn’t a netbook, it is a phone that is actually good.

I’m the happy owner of a BlackBerry Bold. I upgraded from a Curve the day the Bold came out. I’m pleased with the device. It has a great keyboard. The built in push-mail client works well, and the calendar is also very good. Third party apps complete the picture, including google maps and gmail. In fact, the gmail client for blackberry is arguably better than the built in blackberry mail client. The device is small. It has a great screen, and a great keyboard.

But one reason I’m a happy BlackBerry owner is that on the weekends, or when I’m traveling, I have ready access to an iPhone. My wife has had once since they first came out. I can confidently say that the iPhone is a piece of electronics that actually changed my life. With an iPhone, one no longer has to plan trips at home. You can plan them en-route. It becomes possible to choose good restaurants, good activities, and hotels, all on the fly. The iPhone is a device that enables our just-in-time, always-connected lifestyle.

The BlackBerry, on the other hand, is an email appliance. It’s a great email appliance, but it won’t change your life like an iPhone does. The reason, once I got to thinking about it, is that the BlackBerry web browser is crap.

Now, technically it is a fully featured web browser. You can zoom and pan, or reflow text into columns. It implements javascript, css, and all kinds of modern web stuff. But that doesn’t make it a good browser. It is still a chore to use. Some of the challenges are usability. The “back” versus “cancel” behavior always confuses me, for example. And it doesn’t have tabs. But most of the problem’s come down to performance. It is just too slow.

We got a new iPhone 3GS today. The first thing you notice is that it is even more responsive than the original iPhone. Some of that is new hardware, and some is new software. The snappy new iPhone makes the BlackBerry look even worse. So I decided to try to measure the relative performance.

I’d like there to be a mobile-browser benchmark that measured every aspect of the user experience. Unfortunately, there is not. What does exist is the [SunSpider benchmark for JavaScript engines](http://www2.webkit.org/perf/sunspider-0.9/sunspider.html). This benchmark measures the speed of various Javascript operations, and draws conclusions about the implementation. It was developed by the WebKit development team at Apple, so there is a good chance the iPhone is already tuned for it. But it’s a place to start.

![phones4.png](http://innocuous.org/wp-content/uploads/2009/06/phones4.png)The results are pretty telling. In case you hadn’t guessed, lower numbers are better. The BlackBerry JavaScript implementation runs at least three times slower on every test. And on many it is seventy times slower. There are three subtests which it is unable to complete, so I left them out of the measurements. Overall, the BlackBerry is 57 times slower than the new iPhone.

![phones3.png](http://innocuous.org/wp-content/uploads/2009/06/phones3.png)Since it is difficult to see what is going on between the new iPhone and the old, I’ve pulled out those numbers to graph on their own. The obvious thing to notice is that the new iPhone is considerably better than the old iPhone. The old iPhone was running upgraded software, so all the differences are in the hardware, or in the way the software can take advantage of the new hardware.

But I think the most striking difference is to compere the two graphs. I’ve included Firefox here as a baseline. This is Firefox running on my MacBook Pro, a state of the art machine with a state of the art browser. Notice how much better Firefox is than the old iPhone? Well, the old iPhone is *more than that much better* than the BlackBerry.

The BlackBerry hardware is pretty respectable. The only conclusion to draw here is that the implementors at RIM aren’t working very hard on the browser, or have somehow handicapped themselves to the point where they cannot deliver a competitive browser. And without a competitive browser, it won’t be long before the BlackBerry isn’t considered a competitive device.

*For more information on JavaScript Benchmarks in general, see [John Resig’s JavaScript Performance Rundown](http://ejohn.org/blog/javascript-performance-rundown/). If anyone would like to run SunSpider on a G1 or other Android phone, I’d be happy to post the results.*
