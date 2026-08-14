---
title: "Captchas: The Bear Proof Trash Can Problem"
date: 2010-11-21T23:03:00
slug: "captchas-the-bear-proof-trash-can-problem"
wp_id: 86
categories:
  - "Technology"
tags:
  - "design"
  - "metaphor"
  - "optimization"
source_capture: "pages/articles/2010/11/21/captchas-the-bear-proof-trash-can-problem/index.html"
---
[![Not actually my captcha fail, but same idea, a captcha in greek from linked in](/wp-content/uploads/2010/11/linkedin_captcha_fail-300x80.jpg "linkedin_captcha_fail")](https://innocuous.org/wp-content/uploads/2010/11/linkedin_captcha_fail.jpg)Lately I’ve been selling a lot of things on Craigslist. Along with adventures in capitalism, every post to Craigslist requires filling out a [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA), specifically a [reCAPTCHA](https://www.google.com/recaptcha). I’ve noticed that they have gotten quite difficult. In fact, at least one of the captchas I got recently was in Greek.

Captchas area a really clever idea, but they represent a special kind of arms race. The spammers are always improving their automatic and semi-automatic captcha solvers. At the same time, the average web user is not getting any better at solving captchas. The goal of the captcha company is to hit the window between what motivated spammers can do automatically and what web users can do manually.

[![](/wp-content/uploads/2010/11/bear-eat-trash.jpg "bear-eat-trash")](https://innocuous.org/wp-content/uploads/2010/11/bear-eat-trash.jpg)I call this the **Bear-Proof Trashcan Problem**. If you have ever walked up to a trash can in a bearful park, you know the experience. The instructions on the trash cans keep getting longer, the mechanical bits more complicated and more hidden. The result is tourists leaving trash outside the cans, which is as bad as not bear-proofing the cans at all. But if the cans are simpler, or require less manual dexterity, bears figure them out. The bears are willing to put a lot of time into it. And as one park ranger put it, “The smartest bears are smarter than the dumbest tourists.”[![](/wp-content/uploads/2010/11/human-proof-trashcan.jpg "human-proof-trashcan")](https://innocuous.org/wp-content/uploads/2010/11/human-proof-trashcan.jpg)

When you are building software license enforcement, or writing tax law, or creating frequent flyer programs, you face the same problem: the desirable majority is willing to spend much less time dealing with whatever you create than the undesirable minority is going to spend breaking it. Very often people forget this rule, and build systems which focus on preventing the undesirable behavior, driving away the desirable but uncommitted majority. **It’s easy to build a bear proof trash can. It’s hard to build one that a tourist can use.**
