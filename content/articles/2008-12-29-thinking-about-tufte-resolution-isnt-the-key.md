---
title: "Thinking about Tufte: Resolution Isn’t the Key"
date: 2008-12-29T20:56:00
slug: "thinking-about-tufte-resolution-isnt-the-key"
wp_id: 12
categories:
  - "Technology"
tags:
  - "visualization"
source_capture: "pages/articles/2008/12/29/thinking-about-tufte-resolution-isnt-the-key/index.html"
---
A few weeks ago I had the chance to attend Edward Tufte’s lecture in Boston thanks to StreamBase. This was one of his standard lectures on information presentation, for which he has become famous. As usual, it came complete with a set of his books. This was convenient since sometime in my last 4 moves and 3 jobs I lost my set.

I’ve been a fan of Tufte since I first encountered his work as a freshman at MIT. His books contain wonderful examples of good informational graphics, graphics that display quantitative and relationship oriented data, drawn from many modern and historical sources. They are entertaining to read, and provide lots of inspiration for user interface and graphic design.

**PowerPoint**

However, I’ve always found his proscriptions a bit heavy handed though. His strong advice against the use of PowerPoint always seemed to miss the fact that it can be useful. PowerPoint may suck for transferring detailed information. It may even be a bad tool that leads to ugly presentations. But overhead visuals do have merit. They can provide structure that makes it easier for inattentive audiences to follow. There were a few times during the talk, when speaking on topics not found in this books, that he went on too long without any visual aid and PowerPoint could have improved the talk.

**Visual Acuity?**

Several times during the talk, Tufte came back to a claim that the human eye is like a 10 megapixel camera, and that producing bad graphics is like not taking full advantage for that camera. He writes about this on his site in “[Retina communicates to brain at 10 million bits per second](http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0002NC)“. This statistic comes from [a University of Pennsylvania School of Medicine estimate](http://www.physorg.com/news73156830.html). They measured how much data can be transmitted back to the brain by the nerve cells of the retina on a guinea pig, and extrapolated based on the larger size of the human retina. The result is an estimate of eye-brain bandwidth, in terms of raw image data.

That number, while impressive, is misleading. The brain doesn’t use every pixel in the eye independently. If you look at a television screen of static, you might be able to see every pixel, but you can’t count the white ones at a glance. The visual system compresses information, abstracting the pixels into higher level concepts that the brain is trained to understand. That’s why you can read English and use complex computer interfaces, and yet find a page full of Chinese or an airliner cockpit overwhelming.

This compression prevents your visual system from overwhelming your brain with information. Your brain is not prepared to digest every pixel on a static-filled screen. Instead, it can abstract away that piece of your visual field as a known concept, *static-filled screen*. Similarly, when looking at a page of text, you don’t examine every printed pixel, or even every curve of every letter. Your brain sees entire words, looking at collections of letters and using previous experience with the language and content to predict and infer words. This is why a particularly unique turn of phrase or complex sentence can throw off the pace of your reading, forcing you to go back and reevaluate what was actually being said. If we examine common reading speed ([200-250 words per minute](http://www.turboread.com/interpretation.htm)) and the bit density of written English ([about 8 bits per word](http://en.wikipedia.org/wiki/Perplexity#Perplexity_per_word)), we get 2000 bits per minute, or 33 bits per second. So the channel of actual information uptake is much narrower than the bandwidth of the retina.

**Optimized Compression**

While it is narrow, the good thing about this system of observation is that it is optimized for the common cases you encounter, because it is constantly being trained. If you are a native speaker of English, you will have no trouble recognizing a page of English, while a Chinese speaker’s visual system will be more attuned to Chinese. If you are a programmer, even if you have never used it [the Eclipse IDE will likely look familiar](http://www.eclipse.org/screenshots/#), while if you have been a Wall Street trader, then [a Bloomberg terminal](http://en.wikipedia.org/wiki/File:BLOOMBERG.PNG) will seem familiar.

This trained visual system has a big impact on the design of information interfaces. Humans are capable of using very complex interfaces, if they have been trained to use them. Throughout his talk, Tufte kept coming back to the sports pages, pointing out that they are a wonderfully dense source of information, and a good place to go for inspiration. Well, one reason for this is that the last few generations of Americans were introduced to the sports pages as kids, and took the time to understand the information displayed there. We were not born with the ability to interpret a [baseball line score](http://en.wikipedia.org/wiki/Line_score#Line_score), but it would be tough to grow up in America without at least some familiarity. And so any quantitative display that is based on a line score will be easy for people to understand.

When choosing a quantitative display, consider your audience and the displays with which they are already familiar. Familiar information displays will have a fast path through this visual compression. They won’t look confusing, they will look familiar. The information is pre-compressed. It doesn’t look like something else, it looks like people expect information to look.

The benefits of experience explains why new visual communications paradigms like [treemaps](http://radar.oreilly.com/archives/2008/03/state-of-the-computer-book-mar-23.html), [heatmaps](http://screening.nasdaq.com/heatmaps/heatmap_100.asp), or [sparklines](http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0001OR) don’t see much uptake. They are new, and there isn’t a compelling reason for people to learn them. And until a critical mass of people learn them, smart authors won’t use them.

So while I agree with many of Tufte’s conclusions, I think his theory leaves something to be desired. The goal of a visual display of information is not information density. The goal is efficiency of comprehension. And graphical paradigms that people already understand are the easiest way to give them new information.
