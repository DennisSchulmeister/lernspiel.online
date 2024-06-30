# Lernspiel Online: Lecture Game Platform - Core App
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

"""
Here's a quick overview of how the game data model is organized:

## Almost Everything is a Game Component

Games are made up of nested game components. Much like HTML pages are made up
of nested HTML elements (or custom web components). Unlike HTML however, a game
component combines rendering logic and game logic, which are executed on the client
and server side respectively. Also a game component can have more than one "slot"
for child components.

Besides that there is no restriction of what a game component can be. Some components
render a nice frame around the actual game, others render questions, title cards,
player lists, HTML text, high scores, ... or simply manage the game state. Game designers
can mix and match the components and extend them with custom logic to build their games.

## The Holy Trinity of Meta, Definition and Runtime

The game data model has three layers: The meta model, game definition and game runtime.

* __Meta Model:__ This provides the building blocks needed to create games. Developers
  use the Game SDK to develop, test and publish meta model entities, the most important
  of them being generic game components.
    
  Think of the meta model like a code library for game developers.

* __Game Definition:__ This contains the actual games as defined by game designers.
  For this each game uses the game components from the meta model, combining them in
  parent/child relationships (e.g. so that the game frame contains a player list on the
  side and the game content in the middle), providing values for their properties and
  extending them with custom game logic.

  Think of the game definition model like the source code for concrete games.

* __Game Runtime:__ Takes the game definitions to execute their logic. For this a game
  session is created which players can join. The session holds the global game state as
  well as the local game state of each player. Websockets and Django Channels are used
  for real-time communication amongst each other.

  Think of the game runtime like currently running game programs.
"""

from .shared     import *       # Shared models
from .meta       import *       # Meta model
from .definition import *       # Game definitions
from .runtime    import *       # Game runtime