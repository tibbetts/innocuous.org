---
title: "Acela WiFi: Finally Here, Could Be Better"
date: 2010-03-11T16:36:00
slug: "acela-wifi-finally-here-could-be-better"
wp_id: 61
categories:
  - "Technology"
tags:
  - "travel"
source_capture: "pages/articles/2010/03/11/acela-wifi-finally-here-could-be-better/index.html"
---
Riding the Acela to New York yesterday, I had my first opportunity to try out the [new WiFi service](https://www.usatoday.com/travel/news/2010-01-11-amtrak-acela-express-wifi_N.htm). I’m glad to see Acela moving into the 21st century and joining the ranks of BoltBus and LimoLiner by offering WiFi on trips to New York. It’s been a long time coming, and now that it is here I was looking forward to having good bandwidth through the swamps of Connecticut, rather than depending on my fickle EVDO card.

Unfortunately the experience was less than wonderful. Latency was about double that of EVDO, averaging 450 milliseconds with spikes to 2-3 seconds. That meant that ssh connections were difficult to type across and web browsing had a distinctly 20th century feel to it. I wasn’t able to analyze throughput because I couldn’t get most of my web-based tools to load. Suffice to say throughput was disappointing.

I did some tracerouting and analysis, and I think a lot of the problems are in the first hop. First hop latency averaged 200 milliseconds. I’m pretty sure that first hope was on the train, and means that the local 802.11 network is overloaded. I wonder what level of provisioning they planned for. Looking around on Acela it seems like well over 50% of passengers are using laptops, which is a lot of laptops together in a thin metal tube.

The second hop hits a variety of different IPs, which might relate to some kind of multiplexed EVDO connection. These are internal non-routable IPs. The first public IP comes at the third hop, and is a router on [HopOne.net](http://www.hopone.net/) in their Washington, DC area data center. I suspect the second half of the bad latency comes in this WWAN connection and the routing of the messages to DC. I’m not sure how it could be done better, but one imagines it could route directly to one of the national wireless networks. The [MBTA commuter rail](http://www.mbta.com/riding_the_t/wifi/) does this with AT&T, as I understand it.

So overall, I’m glad Amtrak has implemented WiFi, and now that it’s here I hope they improve it to make it usable. I fear they will just start charging to cut down on the overload. But it would be better for the world if they do not, and simply socialize the cost over all passengers. It won’t be long before 100% of passengers have some kind of WiFi device.
