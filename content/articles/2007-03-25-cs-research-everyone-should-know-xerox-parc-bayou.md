---
title: "CS Research Everyone Should Know: Xerox PARC Bayou"
date: 2007-03-25T19:31:00
slug: "cs-research-everyone-should-know-xerox-parc-bayou"
wp_id: 8
categories:
  - "Technology"
source_capture: "pages/articles/2007/03/25/cs-research-everyone-should-know-xerox-parc-bayou/index.html"
---
I was chatting last night with a Web 2.0-oriented friend of mine, and applications that support disconnected operation and synchronization came up. These have been in the noos a bit lately, with the release of the [Ruby on Rails](http://www.rubyonrails.org/) based [Joyent Slingshot](http://joyeur.com/2007/03/22/joyent-slingshot) and talk of the Flash based [Adobe Apollo](http://www.klynch.com/archives/000086.html).

The cliche that those who forget history (or never learn it) are doomed to repeat it is apt. A lot of people thinking about and building these applications have never heard of [Bayou](http://www2.parc.com/csl/projects/bayou/), though they have generally heard of [Xerox PARC](http://www.parc.com/). The project ended in 1997, but there is still a [retrospective page with publications list](http://www2.parc.com/csl/projects/bayou/). From the overview:

> The Bayou system was designed to support collaboration among users who cannot be or choose not to be continuously connected. Network connections may at times be too slow, too expensive, or too faulty for users to effectively utilize, or it may not be possible to establish a network connection at all. \[...\] A major premise that distinguished the Bayou effort from previous work on replicated data algorithms is that disconnected operation by mobile users is a common, rather than exceptional, case.

Bayou identified and solved many of the hard problems of disconnected operation. Of course, the solutions are not web-oriented, and sometimes take the wrong approach. Bayou saw their goal as standardizing a protocol for communication between an application and a data store. In the modern world, this would most likely be done over HTTP/XML/AJAX. But many of the principles are the same. Anyone who is interested in disconnected operation and synchronization should familiarize themselves with [Bayou](http://www2.parc.com/csl/projects/bayou/).
