---
title: "How long will PCs and Servers use the same CPU?"
date: 2009-05-06T13:48:00
slug: "how-long-will-pcs-and-servers-use-the-same-cpu"
wp_id: 43
categories:
  - "Technology"
source_capture: "pages/articles/2009/05/06/how-long-will-pcs-and-servers-use-the-same-cpu/index.html"
---
A couple of weeks ago I attended a meeting at MIT on Cloud Computing. One of the questions from the audience was how cloud computing impacts high performance computing. The response was that in a cloud of inexpensive commodity servers, scientific applications must learn to spread applications across large numbers of parallel compute nodes. This is the most economical way to take advantage of state of the art computing in 2009.

But for how long will this stay the case? The commodity servers at Google are based around Intel (or AMD) x86 chips. These chips represent the most bang for the buck today because they are highly engineered and produced in massive quantities. The production runs at Intel make sense because their chips aren’t just for Google, they power everything from personal computers through small servers up to grid nodes. In fact, the top end CPUs aren’t used in those grid nodes, which favor cheaper processors, but rather in high end servers that will either operate near peak capacity, or which are being purchased to be used for many years.

So Intel makes the same CPUs for everyone. Personal computers drive huge volume. High end servers take the bleeding edge processors before they are available in large volume. Everyone covers the R&D cost of new chip designs and new processes. And cloud computing vendors buy at whatever the current optimal part of the curve is for computing power per dollar.

But is this really sustainable? Personal computers don’t need or want the full power available from a modern processor design. Netbooks and cell phones are the new consumer computing device. Consumers demand long battery life, small size, and low cost, rather than computing power. Intel is responding with new lines of chips, such as Atom, designed for this application domain.

Cloud providers, on the other hand, will continue to want the most computing power they can get per dollar (including power and cooling costs). Thanks to virtualization, they can split a large machine into many smaller machines at low cost. Probably no cost, because a layer of abstraction will be required for management of the cloud nodes anyway.

If Intel is building netbook processors, what will be the most efficient way for cloud providers to get computrons? It probably won’t be large numbers of Atom processors. More likely we will see chips and microarchitectures purpose-built for cloud deployments. Probably machines with large numbers of processors and memory, which run hypervisors natively and are designed for virtualization and partitioning. Machines designed to access networked storage, with lots of communications capacity. Likely machines built up out of hot-swappable, fail-safe components, and encourage long term maintainability and upgradability.

Will Intel be the best company to provide this computer? It seems unlikely. Their position of dominance in the server business is a historical accident, caused by the current period of alignment between the needs of consumers and the needs of large computing organizations.

The cloud computing server I’m describing sounds a lot more like a mainframe than it does like a consumer machine. And while mainframe might be a dated term, we will be seeing a lot of that old being new again in the cloud.

If cloud servers start to look like mainframes, then we should consider what’s going on in the mainframe space. The answer? IBM, who is still building and innovating on mainframes with the [z10](https://www-03.ibm.com/systems/z/hardware/z10ec/). And while IBM’s chip designers can’t compete with Intel on volume, they know a thing or two about building high performance computers, both for consumers ([Xbox 360](http://www.edn.com/article/CA6328378.html)) and for people with big computing needs ([Blue Gene](https://en.wikipedia.org/wiki/Blue_Gene)).

Or might it be Oracle, who has been enjoying the hardware business with their Exabyte machines for the last six months, and who just bought a top quality hardware manufacturer with experience designing novel architectures. If Oracle doesn’t sell it off for cash, I would look to see what the SPARC team is doing next. It might be a rack-sized grid node designed for elastic computing tasks.

So, how long will it be before we see hardware purpose-built for the needs of cloud hosting?
