---
title: "Project Euler, MIT Mystery Hunt Edition"
date: 2010-01-10T23:52:00
slug: "project-euler-mit-mystery-hunt-edition"
wp_id: 58
categories:
  - "Miscellaneous"
tags:
  - "computer science"
  - "MIT"
  - "Programming Languages"
source_capture: "pages/articles/2010/01/10/project-euler-mit-mystery-hunt-edition/comment-page-1/index.html"
---
The [MIT Mystery Hunt](http://www.mit.edu/~puzzle/) starts this Friday at noon, and I’ll be participating seriously for about my 10th year. In the hunt, teams solve a collection of puzzles to discover the location of a gold coin hidden somewhere on campus. The puzzles may be numerous (sometimes over 100), are generally provided without instructions (except when they are provided with [painfully explicit instructions](http://members.bellatlantic.net/~devjoe/dk2/dk2.html)), and the overall structure of the hunt is also unknown at the start. Hunt is nearly always finished before Monday, but during the 60 hours starting Friday at noon, many highly capable teams, some with several dozen members, will try their hardest to solve some very challenging puzzles.

[Project Euler](https://projecteuler.net/) is a neat website that presents a series of computer science problems suitable for students and non-students to practice the skill of writing algorithms to solve numerical puzzles. It’s a great way to learn a new programming language, or just to kill time in a mentally engaging way.

Two of the peculiarities of the MIT Mystery Hunt are that the puzzles are drawn from a wide range of domains, and that there are no restrictions on what resources can be brought to bear on a puzzle. The result is both puzzles that are explicitly about software (e.g. perl program cryptograms) as well as puzzles that are best solved by writing some kind of program. Many of my favorite puzzles over the years have come from this category. Some hunts have few, some hunts have many, but every year there is a call to write some kind of software solution to a puzzle.

The programming skills required to write puzzle solving programs in high pressure situations are different from those normally required to write software, and so it can be useful to practice them. I have collected and categorized here all of the software puzzles since the 2000 hunt. In most cases, I recommend attempting to solve the puzzle, knowing that software is likely the best way. But because the solutions are available, if you are stumped it can still be interesting to read the solution and attempt to duplicate it in software. In most cases the solution is linked from the puzzle page; where it is not I have provided a link. The categories here are presented from least elegant to most elegant, in my opinion. Feel free to jump around and do puzzles which you find attractive.

## Just Decompile It 

A useful trick is to decompile any java applet or flash thing that you are given in a puzzle. The answer might just be in a string constant, though more likely it will just give you a different puzzle to solve.

- [Maze (2005)](http://web.mit.edu/puzzle/www/05/setec/maze/)
- [String Theory (2003)](http://web.mit.edu/puzzle/www/03/www.acme-corp.com/teamGuest/4/4_7.html)
- [Gnireenigne Lab (2003)](http://web.mit.edu/puzzle/www/03/www.acme-corp.com/teamGuest/R/7_175/index.html) This reverse engineering puzzle is pretty challenging. Only one team solved it during the longest hunt on record.
- [Cubology (2002)](http://web.mit.edu/puzzle/www/02/green/B/Puzzle.html) Unfortunately decompiling this one doesn’t really help, but what the hey. ([answer](http://web.mit.edu/puzzle/www/02/green/B/Solution.txt))
- [Twisty Little Passages (2008)](http://web.mit.edu/puzzle/www/08/twisty_little_passages/) Not quite decompilation, but pulling the whole maze down to your local machine is the best way to handle this puzzle.

## MIT Computing

- [Some Trolleys Named Lust (2006)](http://web.mit.edu/puzzle/www/06/puzzles/kuala_lumpur/some_trolleys_named_lust/) The title clues Moira, the computer system that does configuration management for MIT Athena, which has command line utilities named after characters from A Streetcar Named Desire. This puzzle contains components which are no longer online, so you are limited to reading through the solution.

## Mathematical Manipulation and Brute Force Enumeration

Many search problems can be solves on modern hardware with brute force enumeration, or maybe slightly smart enumeration.

- [Bars of Soap (2005)](http://web.mit.edu/puzzle/www/05/setec/bars_of_soap/) Unfortunately the puzzle isn’t available, only the solution, though it still provides a useful programming exercise.
- [Ginormous (2005)](http://web.mit.edu/puzzle/www/05/setec/ginormous/) Prime factorization is always a fun thing to do with numbers.
- [The Road Signs Of Unspeakable Chaos (2003)](http://web.mit.edu/puzzle/www/03/www.acme-corp.com/teamGuest/2/2_5.html)
- [Mathophobia (2001)](http://web.mit.edu/puzzle/www/01/phase3/7/index.html) ([answer](http://web.mit.edu/puzzle/www/01/Solutions/mathophobia.html))

## Text Manipulation

Sometimes a program is the easiest way to do a bulk text manipulation. Particularly when you need to experiment with various transforms, or might need to do them repeatedly. This includes basically all cryptograms, which I am not including here, though software often comes in handy solving them.

- [Blather (2007)](http://www.mit.edu/~puzzle/07/puzzles/blather/)
- [Decode This (2006)](http://web.mit.edu/puzzle/www/06/puzzles/buenos_aires/decode_this/)
- [Long Division (2006)](http://web.mit.edu/puzzle/www/06/puzzles/buenos_aires/long_division/) Not so much text manipulation as diagram manipulation, but you can get the diagram as postscript, which makes it easy to extract the data. Doesn’t help you figuring out the algorithm, but it does make trying out variations easier.
- [Shotgun Wedding (2005)](http://web.mit.edu/puzzle/www/05/setec/shotgun_wedding/) Gene sequencing also comes up occasionally. There are some pretty simple text matching algorithms that turn out to be critical parts of that work.
- [Lost (2004)](http://web.mit.edu/puzzle/www/04/timbuktu/h2H/)
- [Reminders World (2004)](http://web.mit.edu/puzzle/www/04/neotokyo/gE5/)
- [Whoa — I have a Migraine! (2003)](http://web.mit.edu/puzzle/www/03/www.acme-corp.com/teamGuest/Training/tp-c.html)
- [Famous First Words (2002)](http://web.mit.edu/puzzle/www/02/round8/02/Puzzle.html) ([answer](http://web.mit.edu/puzzle/www/02/round8/02/Solution.txt))
- [Lions and Tigers and Bears (2000)](http://web.mit.edu/puzzle/www/00/set2/1/Puzzle.html) My first attempt to solve a puzzle with software, this one wasn’t very successful, partly because of the challenge of getting the grid and the source data accurately input, and partly because of a slow algorithm. The fact that computers were notably slower in 2000 might have also been relevant. I think the most powerful machine available to me was an [Ultra 10](https://en.wikipedia.org/wiki/Ultra_5/10). In the end people doing it by hand finished first. ([answer](http://web.mit.edu/puzzle/www/00/set2/1/Solution.html))

## File Identification and Manipulation 

Many puzzles require you to identify files, or to do interesting manipulations to entire files. Often both at the same time. Sometimes the files are programs written in other languages.

- [Hyperextensions (2009)](http://www.mit.edu/~puzzle/09/puzzles/hyperextensions/PUZZLE/)
- [Surgical Files (2009)](http://www.mit.edu/~puzzle/09/puzzles/surgical_files/PUZZLE/) This puzzle triggered a programming language race, between Perl and Haskell. The race ended in a tie, but I learned some cool Haskell tricks from a teammate in the process.
- [White Noise (2006)](http://web.mit.edu/puzzle/www/06/puzzles/paris/white_noise/) Being able to manipulate audio files with programs or tools is also important.
- [Noise in the Air (2004)](http://web.mit.edu/puzzle/www/04/neotokyo/3wX/) Knowing your off the shelf cryptography tools (ie, openssl) is sometimes helpful
- [Two-Timer (2004)](http://web.mit.edu/puzzle/www/04/vegas/gR3/)
- [A Problem With Printing (2003)](http://web.mit.edu/puzzle/www/03/www.acme-corp.com/teamGuest/2/2_7.html) This is probably my favorite mystery hunt software puzzle. It’s written in the postscript language, which is a great language for puzzlers to know, and makes use of the peculiarities of that language.

## Programming Language Identification and Cryptograms

Many puzzles come down to identifying obscure or not very obscure programming languages. One thinng to be on the lookout for is knitting notation, which can often look like a programming language. Of course, writing programs is often still more efficient than knitting an actual object. Adding complexity, often the programs you are given are cryptograms, or otherwise obfuscated.

- [Tragedy (2008)](http://www.mit.edu/~puzzle/08/tragedy/)
- [Badness 10000 (2006)](http://web.mit.edu/puzzle/www/06/puzzles/kuala_lumpur/badness_10000/) Unfortunately no longer online, but I like the structure. You can read the solution.
- [Square Mess (2005)](http://web.mit.edu/puzzle/www/05/setec/square_mess/) presents you with a machine language and a set of constraints on the notation used for a program in it.
- [Who’s There (2004)](http://web.mit.edu/puzzle/www/04/yukon/Kiz/)
- [Sixty Degrees of Separation (2004)](http://web.mit.edu/puzzle/www/04/timbuktu/LsD/)
- [What Do You Do With A Genteel Sailor (2004)](http://web.mit.edu/puzzle/www/04/pirates/2K2/) [](http://web.mit.edu/puzzle/www/04/timbuktu/LsD/)
- [Whoa — I Know Knitting! (2003)](http://web.mit.edu/puzzle/www/03/www.acme-corp.com/teamGuest/Training/tp-q.html)
- [A Nugget of Wisdom (2002)](http://web.mit.edu/puzzle/www/02/round7/__/Puzzle.html) ([answer](http://web.mit.edu/puzzle/www/02/round7/__/Solution.txt))
- [Use of Gothicism Considered Harmful (2002)](http://web.mit.edu/puzzle/www/02/round2/05/Puzzle.html) ([answer](http://web.mit.edu/puzzle/www/02/round2/05/Solution.txt))

## Honorable Mention

[Blue Steel (2006)](http://web.mit.edu/puzzle/www/06/puzzles/washington/blue_steel/) You can try to solve, but you probably just want to read the solution. It will remind you not to think so hard sometimes.

*\[Edited 2010-01-11 to add Twisty Little Passages (2008). Feel free to add other missing puzzles in the comments.\]*
