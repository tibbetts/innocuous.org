---
title: "Book Review: Defensive Design for the Web"
date: 2005-05-29T11:17:00
slug: "book-review-defensive-design-for-the-web"
wp_id: 38
categories:
  - "Books"
tags:
  - "Web 2.0"
source_capture: "pages/articles/2005/05/29/book-review-defensive-design-for-the-web/index.html"
---
[37 signal](http://www.37signals.com) is one of the neatest  
companies out there in terms of advancing the state of the art in web  
design. It seems like they do almost as much as  
href=”http://google.com”&gt;Google, presumably without spending such  
embarrassing amounts of money. If you haven’t check out some of their  
projects, like [Basecamp](https://basecamp.com),  
href=”http://www.tadalist.com/”&gt;Ta-da Lists, and  
href=”http://backpackit.com”&gt;Backpack, you really should. They  
build really nice web apps. Not only that, but they give back to the  
community with things like  
href=”http://www.37signals.com/svn/archives/000558.php”&gt;the yellow  
fade technique and a presentation on  
href=”http://www.37signals.com/presentations/sxsw2005/37s-bigthingssmallteam.pdf”&gt;How  
to make big things happen with a small team (  
href=”http://www.37signals.com/presentations/sxsw2005/37s-bigthingssmallteam.pdf”&gt;slides)  
(  
href=”http://www.terrystorch.com/2005/03/sxsw\_how\_to\_mak.html”&gt;summary).

[Jesse Vincent](http://www.fsck.com/) just shared with me a  
copy of their book  
href=”http://www.amazon.com/exec/obidos/ASIN/073571410X/innocuousorg-20/ref%3Dnosim/104-5794965-3152724″&gt;*De  
fensive  
Design for the Web: How to Improve Error Messages, Help, Forms, and  
Other Crisis Points*. It was a very quick read this morning  
before breakfast, and I think also worthwhile, even though I am not  
currently a builder of real webapps. I find well designed web  
applications interesting, and like learning more techniques for doing  
it. This book is mostly about user-level guidelines, rather than  
technical detail. But that is important too, since when building  
technical frameworks it is important to enable the right kinds of user  
interaction.

The book is pretty good. It gives a set of 40 guidelines with real  
examples of sites that break and sites that follow the guideline. The  
guidelines mostly focus on what to do when something goes wrong or how  
to keep something from going wrong. The core idea is that when looking  
at the usability of your website, the error cases are as important as  
the non-error cases.

One area in which I disagree is their support of restrictive forms.  
They encourage sites to prevent users from entering incorrect data  
through the use of drop down lists (for things like states or dates)  
and client-side validation with JavaScript. The principle is that if  
you keep users from ever entering bad data, then you are sure they  
won’t have a confusing experience fixing errors. I tend to find that  
these restrictive forms harm my user experience more than they help  
though. I’d rather type a free-form address, or phone number, or date,  
and be corrected, than have to mouse- or arrow-around in 6 drop down  
lists to enter two dates.

Combining client- and server-side validation of form data is an  
interesting challenge for framework development. Is it possible to  
easily combine these so that site developers don’t have two divergent  
code bases (most likely in different languages) to maintain?  
Consolidating this functionality probably requires JavaScript code  
generation, so that the server-side encoding of the validation rules  
can be pushed down to the client. I’m not aware of any JavaScript code  
generation that really makes for a usable system, so maybe this idea  
would be doomed anyway.

Because it ignores technical details and focuses on user experience,

href=”http://www.amazon.com/exec/obidos/ASIN/073571410X/innocuousorg-20/ref%3Dnosim/104-5794965-3152724″&gt;*De  
fensive  
Design for the Web* is a quick read. It’s guidelines are not  
perfect, but they are reasonable. It presents you with a helpful  
checklist which can be used to improve your crisis points, and thus to  
improve your sites whole user experience. And it is lightweight enough  
you can throw it at a coworker without be charged with assault. I  
recommend it for people doing webapp development.
