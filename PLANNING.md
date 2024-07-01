Lernspiel Online: Development Plan
==================================

This living document briefly lists the topics that are currently being worked on
or we we plan to do. Want to pick up a topic? Have more ideas? Let's get in touch. 🤠


Core Architecture
-----------------

### Game Date Model

- [ ] Meta data model
    - [X] Models
    - [X] Admin
    - [ ] API

- [ ] Game definition data model
    - [ ] Models
    - [ ] Admin
    - [ ] API

- [ ] Game runtime data model
    - [ ] Models
    - [ ] Admin
    - [ ] API

### Short-term improvements

- [X] Fixtures for dummy data during development
- Include model primary key in the upload path of media files(!)
- [ ] Automatically fill created_by / modified_by fields in the Admin (and forms in general)
- [ ] Create admin mixin class for CreatedModifiedByMixin model
- [ ] Create admin mixin class for EditKeyMixin model
- [ ] Create model mixin for translation models

### Website

- [ ] Pages and menus
    - [ ] Models
    - [ ] Admin
    - [ ] Views + Templates

### Game Prototype

- [ ] Websocket class in Django which for broadcasts between players (not the final API)
- [ ] Game join screen prototype
- [ ] Game play screen prototype (sidebar with player + game content + simple chat)
- [ ] Hard-coded "Who wants to be a Millionaire" style game
- [ ] Deployment of prototype on lernspiel.online


Game SDK
--------

### Game SDK Library

- [ ] Source structure for game components and game definitions
    - [ ] YAML descriptions
    - [ ] Directory layout for YAML, HTML, JS, CSS, GAMESCRIPT

- [ ] Game SDK CLI
    - [ ] Connect to server via Developer Key
    - [ ] Create and upload temporary game components and games
    - [ ] Watch mode for automatic re-upload on source changes
    - [ ] Publish versioned game components and games

- [ ] Documentation
- [ ] Publish to npmjs.org

### Server-Side

- [ ] Developer API for publishing, unpublishing, ... game components and games
- [ ] Review process to review source code before it is really published
    - [ ] Initially fully manual
    - [ ] Later with AI assistance?


Playing Games
-------------

### Game Script

- [ ] Language Definition
- [ ] Parser (built on top Python's `shlex`) that outputs and AST
- [ ] Execution engine that executes the code in an AST

### Execution model

- [ ] Game runner background workers
- [ ] Game state (global, per player), events, persistence
- [ ] Auto fail-over when a game runner crashes

### Data exchange between players

- [ ] REST API for simple clients
- [ ] Websockets API for realtime clients (and game components browser-side)
- [ ] Library code in the Game SDK to hide the raw API


Game Builder UI
---------------

- [ ] UI Mockups
- [ ] Development