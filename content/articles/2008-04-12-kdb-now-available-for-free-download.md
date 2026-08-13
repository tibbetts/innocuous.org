---
title: "kdb+ now available for free download"
date: 2008-04-12T10:05:00
slug: "kdb-now-available-for-free-download"
wp_id: 15
tags:
  - "Programming Languages"
source_capture: "pages/articles/2008/04/12/kdb-now-available-for-free-download/index.html"
---
If you’ve talked to me about programming languages and Wall Street in the last 4 years, I’ve probably mentioned [kx](http://kx.com/). This is a company which makes a combination programming environment and database based on a language called q which is derived from [APL](https://en.wikipedia.org/wiki/APL_(programming_language)). (Yes, APL, the language invented in 1957 before there was a computer to run it on.) And this environment is in turn used by many of the top quants on Wall Street (and other parts of the financial world) for both research and production systems. Becoming a kx programmer is a good way to double your salary and quadruple your job security.

Well, it’s been going around my corner of the blogosphere that kdb+ is now free for personal use. I first heard about it from [Marc Adler](https://magmasystems.blogspot.com/2008/04/kdb-is-free-for-personal-use.html). You can go download it from the [kx download page](http://kx.com/developers/software.php). This represents a big step towards openness, which I think will be good for everyone.

The q environment is impressive, you have to give them that. There is an emphasis on brevity; the OSX binary of kdb+ is only 227K. That’s smaller than the ncurses library it ships with. And brevity doesn’t stop there. Utterances in the language are well known for their complexity and [impenetrable internal logic](http://kx.com/q/e/book.q). A lot of q code makes obfuscated perl look clear and verbose. It doesn’t help that the culture of kx programmers discourages commenting. Error handling is tricky at best, and modularity and maintainability are in short supply. For confusion, q adds a bunch of SQL keywords on top of the previous language, k, in an almost but not quite fully compatible way.

But for all the faults you can kind find some really interesting features in q. And if nothing else, it is an example of a novel programming language, tightly integrated with a data management system, finding commercial success, which is always nice to see. And if you learn it, you might find a sweet job on wall street as a result.
