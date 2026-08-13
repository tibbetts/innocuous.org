---
title: "Non-Destructive Process Inspection on OSX: Blog Post Recovery"
date: 2010-08-29T22:13:00
slug: "non-destructive-process-inspection-on-osx-blog-post-recovery"
wp_id: 78
categories:
  - "Technology"
tags:
  - "debugging"
  - "osx"
source_capture: "pages/page/2/index.html"
---
Moments ago I was writing a different blog post, about home renovation. Unfortunately just as I posted it a bug in ecto, the aging client I still use to edit blog posts, caused the complete loss of the text with no backup copies. Because messing about with system tools is more fun than rewriting that blog post, I present instead a brief howto for creating a core dump on OSX without killing a process, and inspecting that core dump to attempt to recover your data.

As many of my readers probably already know, a core dump is an image of the contents of a programs memory. Generally core dumps are created when a program fails in a particularly catastrophic way, such as a segmentation fault. Core dumps help programmers find out what lead to the failure. Usually it’s easy to get a core dump, you just do a *kill -11* of the process ID, faking a segfault. This takes down the program and writes a core dump.

Unfortunately since core dumps aren’t useful to non programmers, the environment on OSX by default does not make them, even when there are segmentation faults. One can change this for a given shell or process or login session using the *ulimit* command or the associated syscalls, but Murphy was with me today and so ecto was not running with such a setting. It is possible to change the setting of a running process by connecting with a debugger like *gdb* and making the right syscall, but that felt a little risky, since if I messed it up the process would be gone, whether I got a core dump or not.

Instead, let’s figure out how to not kill the process at all, doing the work of taking the memory snapshot ourselves. This should be possible with modern process inspection APIs. The book you want for this is [Mac OSX Internals](https://www.amazon.com/exec/obidos/ASIN/0321278542/innocuousorg-20/ref=nosim/). I have a copy, and was all set to begin some deep [yak shaving](https://en.wiktionary.org/wiki/yak_shaving) figuring all this out. However, the book saw me coming, and already laid out an example in detail, called [Process Photography](http://osxbook.com/book/bonus/chapter8/core/).

So, if you want to know a lot more about making your own core dump utility, you can read that post. Or if you are still with me because you just want to know how to recover a blog post, then go there and download [gcore-1.3.tar.gz](http://osxbook.com/book/bonus/chapter8/core/download/gcore-1.3.tar.gz "gcore-1.3.tar.gz") at the end of the post. Untar it and compile your *gcore* utility. Now you can create a core dump by running *gcore -c ecto.core PID*. If your experience is like mine, this will generate a 1.3 gigabyte core file, because modern programs are not shy about using memory, virtual and otherwise.

Now, this 1.3 gigabyte core file contains everything from program text and mmaped files to active memory to freed memory that hasn’t been reused yet. It’s a vast expanse of stuff you don’t need, must of it binary. Luckily, most programs will just store textual content as ASCII or UTF8. Assuming you were writing English, then the *strings* utility will be sufficient to find your text. So you can run *strings ecto.core &gt; ecto.strings*. This will generate another large file (64 megs this time, not 1.3 gigs) with just the ascii string data from your programs memory. Still a lot to wade through, so I use *grep -i* to look for uncommon words in my post, and *less* to be able to page around the file quickly.

I wish that the story had a happy ending, but after all that I found that the ecto memory space contained a dozen copies of my post, but all of them were the truncated version that it had posted on my blog, rather than the actual text I wrote. So you will have to wait until next week (or at least tomorrow) to learn what I had to say about house renovation.
