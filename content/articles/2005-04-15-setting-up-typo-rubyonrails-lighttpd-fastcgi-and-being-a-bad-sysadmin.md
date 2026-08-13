---
title: "Setting up Typo: RubyOnRails, lighttpd, FastCGI and being a bad sysadmin"
date: 2005-04-15T09:10:00
slug: "setting-up-typo-rubyonrails-lighttpd-fastcgi-and-being-a-bad-sysadmin"
wp_id: 39
categories:
  - "Technology"
tags:
  - "lighttpd"
  - "ruby on rails"
  - "typo"
  - "Web 2.0"
source_capture: "pages/articles/2005/04/15/setting-up-typo-rubyonrails-lighttpd-fastcgi-and-being-a-bad-sysadmin/index.html"
---
I took most of my evening last night to set up FastCGI and [lighttpd](http://www.lighttpd.net/). My goal was to serve a [Typo](http://typo.leetsoft.com/), a blog engine based on [RubyOnRails](http://rubyonrails.org). I was thwarted by not knowing RubyOnRails very well, and by knowing FastCGI and lighttpd not at all.

The first issue was that Typo doesn’t like to run in a subdirectory on a webserver. That is, it wanted to be at `ntsh.innocuous.org/`, not `innocuous.org/ntsh`. This offended my sensibilities somewhat, so I decided to beat it into submisssion. This involved tracking down a bunch of places where paths were hard coded, which included a few places in the templates and the CSS.

The second issue was that FastCGI on lighttpd seems to have been designed for php. You can easily tell it to delegate `*.php` to FastCGI. You can tell it to delegate `/ntsh/*` to FastCGI, but that has the problem that `/ntsh/stylesheets/base.css` doesn’t work, because the RubyOnRails dispatcher doesn’t know how to serve static pages.

You also have the problem, and this is the showstopper, that for some reason the `AbstractRequest.request_url_base` function helpfully strips off the directory of your request path when you use it this way. That is, it turns `xml/rss/feed.xml` into`feed.xml`. As you might imagine, losing the `xml/rss` part confuses the cool new [routing feature of Ruby on Rails](http://manuals.rubyonrails.com/read/chapter/65). So this was unacceptable.

I had to give up my delusions of configuring lighttpd in some clean way, and instead use the trick that a bunch of web pages recommended: `server.error-handler-404`. This configuration file setting tells the server to delegate 404 errors somewhere, and that somewhere can be the Typo dispatcher. Combined with the conditional configuration functionality of lighttpd, this is actually quite sufficient to get Typo up and running. But it still feels like a hack for some reason.

The conclusion I’m coming to, as I’ve come to many times before, is that I’m a bad sysadmin. I expect to be able to bend software to my will, and make it work the way I want, which should be elegant and conform to my expectations. When doing sysadmin work, it is important to use the software you are given, the way someone else designed it to be used. But it always has to get to be 1am before I remember this principle.

For anyone who is interested, here is the relevant chunk of lighttpd.conf:

    $HTTP["host"] =~ "\.innocuous\.org$" {
        server.document-root = "/var/www/vhost/innocuous.org/pages"

        $HTTP["url"] =~ "^/ntsh/" {
            server.error-handler-404   = "/ntsh/dispatch.fcgi"
        }

        fastcgi.debug = 0
        fastcgi.server = (
                    "/ntsh/dispatch.fcgi" =>
                        ( "ntsh" =>
                            (
                                "socket" => "/tmp/ntsh.socket",
                                "bin-path" =>
                                  "/var/www/vhost/innocuous.org/ntsh/public/dispatch.fcgi",
                                "min-procs" => 1,
                                "max-procs" => 5,
                                "max-load-per-proc" => 4,
                                "idle-timeout" => 20,
                                "bin-environment" =>
                                  ( "RAILS_ENV" => "production",
                                    "RAILS_ROOT" => "/var/www/vhost/innocuous.org/ntsh"),
                                "check-local" => "disable"
                            )
                        )
            )
    }
