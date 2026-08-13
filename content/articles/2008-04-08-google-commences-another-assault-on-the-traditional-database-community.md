---
title: "Google commences another assault on the traditional database community"
date: 2008-04-08T09:32:00
slug: "google-commences-another-assault-on-the-traditional-database-community"
wp_id: 17
tags:
  - "Database"
source_capture: "pages/articles/2008/04/08/google-commences-another-assault-on-the-traditional-database-community/index.html"
---
Many in the blogosphere noticed when [Stonebraker and Dewitt at The Database Column](http://www.databasecolumn.com/) took offense at the idea that [map-reduce is the solution to many of life’s problems](http://www.databasecolumn.com/2008/01/mapreduce-a-major-step-back.html). The idea that a simple idea, promoted by a services company, can blow away 20+ years of distributed database research, bothers them for some reason. Sure, it may not be the best solution to every problem, but it is a sufficient solution to many problems.

Google is quietly at it again, this time with the [Google AppEngine](https://code.google.com/appengine/docs/whatisgoogleappengine.html).

This time, they are taking a shot at transaction processing. This is particularly amusing, because Stonebraker himself has been predicting an upset in transaction processing for a few years now. But rather than demonstrate tight integration between a app language and the database optimizer, or use traditional stored procedures, Google is again causing problems by building the simplest thing that can possibly work. And simple developers with simple applications are going to like it.

The [Google App Engine data store](https://code.google.com/appengine/docs/datastore/) is a non-relational database, with support for an SQL-like but limited language called (unsurprisingly) [GQL](https://code.google.com/appengine/docs/datastore/gqlreference.html). There are no joins. [The lock management is simplistic](https://code.google.com/appengine/docs/datastore/transactions.html). It is basically an entity-relationship database, with fixed and variable attributes associated with each entity. Every query is always a SELECT \* (“The SQL syntax is retained for familiarity”).

The whole thing is wrapped in a Python object-mapper, which means it looks quite a bit like an object database with a simplified model. This turns out to be what most people who are building web applications, whether in PHP, Ruby on Rails, or Java (Hibernate). Delivering a database which is limited to this functionality puts google in a powerful position to optimize specific use cases for simplicity and performance.

We are at the start of (or possibly in the middle of) a cycle that we haven’t seen in over 10 years: Existing assumptions about databases are being questioned, and a thousand flowers are blooming. Stonebraker himself pointed this out in his [One Size Doesn’t Fit All](http://www.databasecolumn.com/2007/09/one-size-fits-all.html) papers, talks, and columns. However, it is not just the Oracle of the world who need to change or get out of the way. It is also the leaders of the database research community and their dominant paradigms. Things are going to be messy for a while yet. But in the end we will have technology that better fits modern infrastructure and modern usage.
