Lernspiel Online: Game SDK
==========================

1. [Lernspiel Online Lecture Games](#lernspiel-lecture-games)
1. [The Lernspiel Game SDK](#the-lernspiel-game-sdk)
1. [Getting Started](#getting-started)
1. [Copyright](#copyright)

Lernspiel Online Lecture Games
--------------------

A good lecture is driven as much by the learners as by the teachers. It thrives on participation and
interaction. However, this is exactly what many students find difficult, as they either lack motivation
or have a very high inhibition threshold to break out of the anonymous crowd. Lernspiel Online helps
teachers to make their lectures more interesting through interactive lecture games and thereby improve
the active participation of students. Lernspiel Online offers the opportunity to easily create appealing
and entertaining learning games that can be used in a classroom setting to reflect, test and deepen one's
own knowledge with and against each other in a fun and entertaining way.

Key differences to other lecture game platforms are:

1. **Free Software:** Lernspiel Online is 100% free and libre software, developed in a university setting
   with no commercial background. All features are free (as in beer and in freedom) forever.

2. **Privacy:** Lernspiel Online respects the privacy of teachers and learners. Cookies are only used
   where technically necessary. No advertisements, user tracking, usage analytics and other
   mis-features.

2. **Multiplayer:** The main product idea of Lernspiel Online is for a teacher to play educational games
   with a classroom, e.g. at the start of a lecture to activate the audience and recollect key points from
   the previous lesson. Instead of each student playing alone, the teacher hosts and moderates a game in
   which the whole class can play together. Outside lessons students can still access and play the game alone.

3. **Hackable:** The Lernspiel Online source code is easy to understand and extend and the server-side
   platform is separate from the game code. New game types can easily be developed and installed without
   changes to the server. The idea is that Lernspiel Online can be used in programming courses to let
   students build new game types or otherwise use the platform for practical projects.

   But don't be afraid. Of course, Lernspiel Online can perfectly be used as is to build games for any
   lecture. Supporting programming projects is just another feature, that can but don't need
   to be used.

4. **Engaging Community:** Lernspiel Online's home base is DHBW Karlsruhe (Cooperate State University
   Baden-Württemberg Karlsruhe) in south Germany, but anybody is welcome to join the project. We are
   always happy to engage with the community. Need help in setting up Lernspiel Online? Have ideas
   about new features? Want to work on the platform itself? Anything else? Let's get in contact.

The Lernspiel Game SDK
----------------------

Lernspiel Online makes a clear separation between the core server and game code running in the browser.
This allows to easily add new game types without redeploying the server. New game types can easily be
defined in the Admin UI, by uploading new game libraries. The Game SDK on the other hand is used by
developers to program and test the client-side game code. No server knowledge (Python, Django, Database, …)
is needed at all. But a running server, allowing game developer access and at least one example game are
required to get started.

The Game SDK provides pre-configured tooling for [TypeScript](https://www.typescriptlang.org/) and
[esbuild](https://esbuild.github.io/) and skeleton code to build new game types. It also contains a CLI
that connects with a Lernspiel Online server to allow playing games with the locally developed code.

Getting Started
---------------

TODO - It's the early days. The Game SDK still needs to be written.

Copyright
---------

Lernspiel Online: Lecture Game Platform <br/>
© 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de> <br>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Development funded by the KoLLI research project at DHBW Karlsruhe.
