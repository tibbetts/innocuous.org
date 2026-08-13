---
title: "Making offlineimap not die"
date: 2006-01-20T12:29:00
slug: "making-offlineimap-not-die"
wp_id: 33
categories:
  - "Technology"
tags:
  - "email"
  - "imap"
  - "mutt"
source_capture: "pages/articles/2006/01/20/making-offlineimap-not-die/index.html"
---
I love [offlineimap](http://gopher.quux.org:70/devel/offlineimap/). I even love the quirky way it is hosted on a gopher site. The functionality is awesome. For those of you who don’t know, offlineimap syncronizes a remote IMAP mailbox heirarchy with a local Maildir folder heirarchy. This means you get disconnected IMAP operation with all your favorite Maildir clients (like [mutt](http://mutt.org)), while still retaining the ability to access your mail using other IMAP clients.

However, offlineimap crashes too often. Every couple of days I will fail to get any new mail for an hour or two, and realize that offlineimap has crashed. And due to Murphy’s law this generally correlates with a time when I was recieving some important mail.

The solution is very simple. I am using [zenity](https://directory.fsf.org/zenity.html), a command line tool for displaying dialog boxes, and running offline imap in a loop. Every time it dies, I get a pop-up dialog, and can say OK to restart it, or Cancel to end the loop. The little shell script to do this is as follows:

\#!/bin/sh

/usr/bin/offlineimap -u TTY.TTYUI;

while zenity –question –text “Offlineimap died. Restart?”; do

/usr/bin/offlineimap -u TTY.TTYUI;

done
