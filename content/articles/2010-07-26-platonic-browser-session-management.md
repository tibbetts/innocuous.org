---
title: "Platonic Browser Session Management"
date: 2010-07-26T01:04:00
slug: "platonic-browser-session-management"
wp_id: 75
categories:
  - "Technology"
tags:
  - "computer science"
  - "Web"
source_capture: "pages/page/2/index.html"
---
Firefox just crashed, and when I restarted it I was informed that it had some trouble reopening my 115 tabs. Understandable, but I went ahead and clicked the button that encouraged it to try harder. The result, after consuming what would have been several thousand dollars of computer time back when they charged for it, is that I’m back in the mess I made myself, with an unmanageable collection of pages open, covering topics like faucets, washing machines, coffee brewing, JVMs, whatever else came out of Google Reader, and the research I was doing for this post.

Our civilization has had tabbed interfaces since [1988](https://en.wikipedia.org/wiki/Tab_(GUI)#History). Mainstream browsers (well, Mozilla) have supported tabbed browsing since 2001. As tabbing has become more mainstream, as the web has gotten more complex, and as computers have gotten fast enough to handle dozens of open web pages, people have opened more and more tabs. The result is that nearly everyone knows the experience of “just having to close some tabs” before you reboot, or so you can get on with more important work. It’s easy to overwhelm yourself with the amount of content you can have open in tabs, and clearing it out is often an archeological experience spanning the last week or month of your web activities.

Browser tab management represents the greatest software usability challenge of our time. We are all facing information overload of one form or another, and this is an opportunity to improve the way people find, consume, retain, and manage information. Lately we are seeing a lot of attempts at innovation here, from Chrome’s tear-away tabs and performance optimization, to Firefox extensions like [Ctrl-Tab](https://addons.mozilla.org/en-US/firefox/addon/5244/). Most recently today we saw [Tab Candy](http://www.azarask.in/blog/post/tabcandy/), a preview of new functionality in [Firefox 4](https://www.mozilla.com/en-US/firefox/beta/features/).

I’ve often said that I’ll switch to the first browser that doesn’t make me feel guilty for having 100+ open tabs. Looking at Tab Candy and other innovations, I see that we are moving in the right direction. But there are still many aspect of the problem that aren’t being sufficiently addressed.

- Application-oriented tab organization – Many of the sites I use today are really applications, whether it is Google Docs, Facebook, or Amazon. Taking application behavior into account, and helping me to avoid opening the same heavy application (e.g. gmail) multiple times is part of getting tab management correct.
- Automatic tab organization – Systems like Tab Candy require that users manage tabs. But wouldn’t it be better if tabs were managed and grouped automatically?
- Managing the tab/bookmark continuum – Leaving something open in a tab, or opening it in a tab, is often a way of deciding to come back to it later. Bookmarks accomplish the same thing, but most people’s bookmarks are themselves a usability nightmare. Automatically migrating tabs into bookmarks and bookmarks back into tabs might be the solution to a lot of these tab problems.
- Excursion and history management – Web browsing isn’t a linear process, the way browser history would have you think. It is at least a branching tree, which tabs support. But often the process of web browsing is a product itself, as when researching a new subject or deciding on a purchase. Being able to not only manage the process as it is happening, but also to archive it for later resumption or reference, would improve the efficiency of many browser tasks.
- CPU efficiency – An implementation detail to be sure, but one of the obstacles to running with 100+ tabs is the CPU load of all the little Javascripts. Some way to manage this, pausing or closing pages which are not visible, is likely to be required.

As you can see, there is still plenty of room for improvement in the browser interface, particularly around large numbers of tabs. What other cutting edge stuff have you seen? What would you like to see implemented?
