---
title: "Identify and Manage the Honey-Badger Developer"
date: 2015-03-28T12:10:00
slug: "identify-manage-honey-badger-developer"
wp_id: 171
categories:
  - "Management"
source_capture: "pages/index/index.html"
---
A few years back I read [Rands’ blog post about the Free Electron developer archetype](http://www.randsinrepose.com/archives/2005/03/20/free_electron.html): “the single most productive developer you’re ever going to meet.” This is a good archetype to understand, identify, recruit, and retain. I would like to discuss another related archetype which can be quite powerful if properly harnessed: The Honey Badger.  

*[“There is no other animal in the kingdom of all animals, as fearless as the crazyass Honey Badger.”](https://www.youtube.com/watch?v=4r7wHMg5Yjg)*

Like the honey badger itself, the honey-badger developer has no fear. They will undertake any project, with any technology, on any deadline. They will not be paralyzed by the impossibility of choosing a good architecture. They will proceed single-mindedly in the direction of the current stated requirements, even as those requirements change.

What makes for a honey-badger developer?

- Willing to work with grotty systems
- Uses undocumented APIs
- Reverse engineers protocols
- Finds third party libraries whenever possible
- Able to glue anything to anything else
- Able to work within really challenging constraints
- Pursues a successful implementation regardless of architectural purity
- Gets things done

Of course, these are not universally positive traits. If you are developing the foundation of a new software platform, a new hypervisor or database kernel, you won’t want to make these kind of tradeoffs. On the other hand, if your largest customer absolutely requires an integration with their unmaintained COBOL running on an IBM mainframe by the end of the quarter, then a honey badger may be just what you need.

Sometimes it can be hard to tell the difference between a honey badger and a non-badger who is struggling. The difference is in what they attempt and accomplish. A struggling developer may try some of these behaviors, but their project isn’t actually that difficult and a better developer could just do it properly. A honey badger, on the other hand, brings out these tools in clutch situations where other developers throw up their hands in despair.

How do you properly manage a honey badger? What a honey-badger developer needs is audacious requirements, guardrails, and admiration. What they don’t need is unrestricted commit access. Create the right environment, and they will be a powerful force for project success.

Audacious requirements are the honey for the badger. They are happiest when attempting projects other people think are impossible. So make sure you pick good projects. The best projects will have deadlines. Integrations are often good, particularly when one or both systems are proprietary and poorly understood. Performance challenges can also be a fit, particularly in scaling and throughput (latency often requires more detail work). Demonstrations and proof of concept work often create the right context, with lofty aspirations and tight deadlines. Make sure the honey badger understands whether the goal is to do the work or to show the work. It may make a big difference in how they approach things and where they spend their limited time.

The guardrails for a honey badger should give them plenty of room to choose implementation, but a bright line not to cross. For example, your code must run in a separate process, or it must run on a separate machine. It must expose this API, or use this API. It must run in this VM or this container. And be clear. If you want the code to be in Java, you have to say that, otherwise your requirement that it work with a JVM may result in the use of Clojure because the honey badger found a library that did most of the work.

Finally, a honey badger needs admiration. They are going to do things which are hard, and unpleasant. They will likely work long hours to meet a deadline, or travel to work directly with an inaccessible customer system. They know they are creating solutions which are not the most elegant code. They need to hear from you, and from the team, that what they are doing is important and they are doing an impressive job.

The one thing not to do with a honey badger is invite them to make changes on your core systems. This is a corollary to the guardrails requirement. If the honey badger has the ability to change something, they will, and often not in a way that everyone on the team appreciates. Unfortunately, it will be in service of some critical requirement. So get in front of those conflicts, and either create a process for approving their changes, or just enforce a guardrail.

When your honey badger has succeeded, you will have a working system, sometimes just a single unreproducible instance. To defend against this, try to get them committing early and often, even if it is to a private repository. Your system, if it was built for a customer, may be distressingly close to production. Your customer will also have fallen in love with the honey badger and not want to let them go. You must either fit this into the economics of your  business, or ideally find ways to wean them off the honey badger.

The honey-badger developer can be tremendously valuable asset to any software team, and especially a software business, if managed correctly. What other success stories do you have about honey badgers? Other management tips?
