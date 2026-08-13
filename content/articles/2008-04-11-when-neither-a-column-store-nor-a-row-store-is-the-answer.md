---
title: "When neither a column store nor a row store is the answer"
date: 2008-04-11T22:34:00
slug: "when-neither-a-column-store-nor-a-row-store-is-the-answer"
wp_id: 16
tags:
  - "Database"
source_capture: "pages/articles/2008/04/11/when-neither-a-column-store-nor-a-row-store-is-the-answer/index.html"
---
A few days ago I found myself giving database advice to a friend with a new startup. His problem is a pretty common one: he has a very large corpus of data, over which he will run compute-intensive proprietary algorithms. Both the data and the computation will require a cluster of machines. He has a prototype based on Postgres. His question to me: should I continue to use a row store (Postgres) or should I use new technology, specifically a column store?

If you read the title of the post, you can already guess that my answer was neither.

Traditional row stores are optimized for transaction processing, in which records are updated. They are also sufficient for small data sets and ad hoc queries, as you find in a normal web app. Column stores are optimized for ad hoc queries, but this time against very large sets of data.

In either case, the data store is designed as a shared resource to cope with IO bound operations. But for many applications, the database is neither shared nor IO bound. In this application, the large data store is used by a small set of applications (the data loader and the data reducer), which are long running with predicable access patterns. This is in sharp contrast to the kind of load databases are designed to support.

The answer is to look at much simpler tools like [BigTable](https://en.wikipedia.org/wiki/BigTable), which are optimized for precisely this kind of access pattern. BigTable stores data in columns, but spends considerably less effort optimizing the IO of the data. Instead, it assumes the application will access the data in a reasonably efficient way. It’s great if you have a single application or single kind of application working over your data. In fact, BigTable even interoperates well with Map/Reduce, which is a reasonable basis for the compute intensive part of this application. The [Hadoop](https://hadoop.apache.org/) implementation of these technologies looks pretty good.

There is an ad hoc query component to the application, but it is ad hoc queries of the results of the data reduction. The results are effectively a pre-aggregation of the large data set. There is a two-tiered storage model already built in to the design.

Now, an idealized database management system, the kind that you get along with your flying car, might make this two tiered design unnecessary, or at least automatic. It ought to be able to index the huge data set and support queries against it, notice patterns in those queries and store pre-aggregated information in order to service common queries quickly. But no readily available system comes even close to that level of self management. In fact, you would have a hard time finding a DBMS that gives you really rich and pleasant to use semantics for maintaining materialized views, never mind automatically creating them.

So, for now we build knowledge of these limitations into our system architecture, take a two tiered approach, and can benefit from the good work done by Google at building a very large, very dumb data store.
