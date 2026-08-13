---
title: "Transactional Memory Not Solution To All Problems"
date: 2006-12-01T20:10:00
slug: "transactional-memory-not-solution-to-all-problems"
wp_id: 10
tags:
  - "Database"
  - "Programming Languages"
source_capture: "pages/articles/2006/12/01/transactional-memory-not-solution-to-all-problems/index.html"
---
I was at MIT today and so I ended up going to an invited talk on computer architecture, [Subtle Semantics and Unrestricted Implementation of Transactional Memory](https://www.csail.mit.edu/events/eventcalendar/calendar.php?show=event&id=1298). [Transactional Memory](https://en.wikipedia.org/wiki/Transactional_memory) is a very hot topic in systems and architecture. It is perceived to be a better model for programmers, so language designers like it. And there are a variety of options for pure-software and hardware-assisted implementations. And because it enables optimistic concurrency control, transactional memory can help make programs faster and more scalable on new multi-core architectures. There is every reason to believe that processor vendors will begin including some form of hardware support for transactional memory.

The focus of the talk was on the subtle issues that come from this. It dismissed a few of the more positive myths about transactional memory:

- Programs using locks cannot be trivially converted to use transactions. In fact, a correctly behaving program using locks to manage things like inter-thread communication can easily deadlock or livelock when using transactions.
- Transactions are not perfectly composable or nestable, as is often claimed. This means heirarchical or nested transactions, where there is a program-level transaction wrapping several library-level transactions, can lead to deadlock or livelock.
- Whether a transactional system is weak (non-transactional code executes concurrently with transactional code, with side effects visible between) or strong transactional (a transaction is atomic not just from the perspective of other transactions, but also to other non-transactional code) can have a significant effect on program behavior. Not only can a program designed for strong transactions have problems under weak transactions, but a program that behaves correctly in a weak transactional system may deadlock in a strong transactional system.

This leads me to two primary conclusions, with which I think the speaker would agree: First, transactional memory can have significant confusing side effects, just like locks, and so it is not a solution to the difficulties of multithreaded programming. Second, if processor vendors implement, and many programmers use, weak transactions then we may never get strong transactions.

I’d like to take this one step further. I think language designers and computer architects who are excited about transactional memory are missing the point. They are trying to create a single concurrency control mechanism that can solve everyone’s problems. In fact, I think there are two separate classes of problem that are best addressed separately: Concurrency control for systems programming, and concurrency control for application programming.

Systems programmers are close to the hardware, inside or right on top of the operating system. They are the people who are most comfortable with the concurrency control mechanisms of today ([pthreads](https://en.wikipedia.org/wiki/Pthreads) and [java.util.concurrent](http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/package-summary.html)). Transactional Memory should be targetting these users. The goal is not to give them an easy way to do concurrency, but to make optimistic concurrency control possible and efficient. Continuing to discuss the merits of strong and weak transactions is reasonable, but it should be in the context of what most efficiently represents the capabilities of the hardware.

Application programmers generally work on top of a platform, and don’t have to think about concurrency in the same way. if they don’t work on a platform then they should. For example, application programmers are often writing business applications as web services on top of J2EE. By using platforms, they can work with much higher level management and concurrency control. The most common idiom for concurrency control is the database transaction (or distributed transaction). It is able to handle most concurrency problems in traditional RPC-and-datastore systems.

To help application programmers, we need to develop additional idioms. Not all programs can utilize the J2EE style of platform. I expect to see a significant advance in scientific computing tools like MATLAB to take advantage of multiprocessor systems (in my ideal world it would be by vectorizing based on static and dynamic analysis, but I digress). Furthermore, there are a large set of event processing (stream processing, complex event processing) which are also not well served by J2EE-type platforms and database-transactions. Which is why I work on [StreamBase](http://www.streambase.com/) (and on [StreamSQL](http://streamsql.org)), which is creating next generation programming models for those kinds of applications, to enable parallelization, managability, and scalability.&lt;/shameless-plug&gt;
