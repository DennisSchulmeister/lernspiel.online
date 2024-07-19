Developer Notes for Lernspiel Online
==========================

This document serves as a cheat sheet for developers to get started quickly. There are no
fancy things -- if you already know Python, Poetry, Django, NPM, … But finding the right
information might not be easy when working with so much different technology. This document
tries to summarize the most important things.

1. [Quick Start](#quick-start)
1. [Technology Choices](#technology-choices)
1. [Directory Layout](#directory-layout)
1. [Poetry Package Management](#poetry-package-management)
1. [Django Web Framework](#django-web-framework)
1. [Django Project vs. App](#django-project-vs-app)
1. [Creating Fixtures](#creating-fixtures)
1. [SQLite Shell](#sqlite-shell)
1. [NPM and esbuild](#npm-and-esbuild)
1. [The Game Server Data Model](#the-game-server-data-model)
1. [Developing New Game Components](#developing-new-game-variants)

Quick Start
-----------

The following tools must be available on your development machine:

* Python
* Node.js
* Redis

Then you can install all dependent libraries:

```sh
poetry install
npm install
```

To run all components locally:

```sh
npm start
```

This will start the following things:

* Daphne Webserver in watch mode
* Redis Key/Value-Store
* Two game runner instances
* A local fake SMTP server
* Esbuild in watch mode

The setup will be fairly similar to a typical production environment minus the database.
For local development we use SQLite as per Django's defaults.

Technology Choices
------------------

Lernspiel Online is built with the following technology:

* Python
* Poetry - Package Management
* Django Web Framework - Core Technology
* Django Channels - Websocket Support
* Django Ninja - REST API Support

The idea is to keep the technical requirements lean to enable easy deployment in custom environments.
Therefor the choice of Django might be considered "conservative", but in fact it contains all the needed
functionality like HTTP request routing, server-side templates, database access, ... in a single, stable
and well maintained dependency. 

For the frontend we use the following additional things:

 * esbuild - Bundler
 * npm - Package manager
 * TypeScript - Type annotations for JavaScript

Technically this requires to have Node.js installed, but we are not developing much with Node.js.
It is mostly used to access the npmjs.org package repository and install the esbuild bundler.
Except for the Game SDK, where Node.js is used to connect with the Lernspiel Online platform.

Directory Layout
----------------

Here are a few important directories and files that you might want to know about:

```text
.                                       Root directory with this file
├── lernspiel_server                    The server application
│   ├── lernspiel_server
│   │   ├── local_settings.py           Use this for your own server configuration
│   │   ├── settings.py                 Internal settings of the server
│   │   └── ...
│   └── manage.py                       Django CLI for the server
│
└── game_sdk                            Lernspiel Game SDK
    ├── cli                             Game SDK CLI
    └── web                             Game SDK Client Library
```

Poetry Package Management
-------------------------

Python dependencies are managed with [Poetry](https://python-poetry.org/), which is similar in spirit
to NPM for Node.js developers. It handles installation and upgrades of all required external Python
packages, which for this reason need to be declared in the [pyproject.toml](pyproject.toml) file,
plus it fully automates the usage of virtual environments. The most important commands are:

* `poetry init` - Start a new project with the Poetry package manager (already done of course 🙂)
* `poetry install` - Install all dependencies specified in [pyproject.toml](pyproject.toml)
* `poetry add xyz` - Add another dependency to library `xyz`
* `poetry remove xyz` - Remove dependency to library `xyz` again
* `poetry show --tree` - Show all direct and indirect dependencies
* `poetry shell` - Start a new shell with the Python environment enabled
* `poetry run xyz` - Run console command `xyz` in the Python environment

Django Web Framework
--------------------

[Django](https://www.djangoproject.com/) is our server-side main framework. It comes with its own
CLI called `django-admin` or `manage.py` inside the project directory. Actually both are identical,
but with the latter a few environment variables point to the current project.

Important commands at the root-level, outside Django projects:

* `django-admin xyz` - Run Django admin command `xyz`
* `django-admin startproject xyz` - Add new Django project `xyz` to the workspace

Important commands inside project directories:

* `./manage.py xyz` - Run Django management command `xyz`
* `./manage.py startapp xyz` - Add Django app `xyz` to the Django project
* `./manage.py runserver` - Start development server
* `./manage.py test` - Run unit tests
* `./manage.py collectstatic` - Collect static files into `_static/` directory
* `./manage.py dbshell` - Open a database shell to inspect the database

After each change to the database model, the following commands need to be run:

* `./manage.py makemigrations` - Create migrations from latest model changes
* `./manage.py migrate` - Run database migrations

Once the changes shall be committed to version control, it makes sense to "squash" the migrations,
to have only one migration file for all changes:

* `./manage.py squashmigrations` - Reduce multiple migrations into one

Django Project vs. App
----------------------

Each Django web application consists of a _Django project_, representing the web application
itself, and usually multiple _Django apps_, representing single functional units. Both are
Python modules with certain required source files. Though the whole source code could easily
live inside the project module, the Django developers recommend splitting the project into
multiple apps to foster separation of concerns and code re-use.

When you have a project like `lernspiel_server` the Django Admin command created a top-level
directory of that name, containing a sub-directory of the same name. Next to it the Django
applications will be created:

```text
.                                       Root directory with this file
└── lernspiel_server                    Django project top-level
    ├── lernspiel_server                Django project python package
    │   │   └── settings.py             Configuration file
    │   └── ...
    ├── manage.py                       Django CLI for the server
    │
    ├── ls_app_1                        Django Application
    │   └── ...
    ├── ls_app_2                        Django Application
    │   └── ...
    └── ls_app_3                        Django Application
        └── ...
```

Creating Fixtures
-----------------

Fixtures are a good way to provide initial data for developers and end-users to get started with
the Lernspiel server. Here are a few hints on what to consider:

* **Hand-edited YAML Format:** Use `python manage.py dumpdata --format yaml myapp` to create a data
  dump on the console. Copy the relevant parts into a new `fixtures/myapp/xyz.yaml` file. Note that
  the file extension must be exactly `.yaml` for Django to recognize the fixture. Clean up the file,
  bring all entries in logical order, remove unneeded `null` properties and add comments.

* **Natural Keys:** When using the `dumpdata` command make sure to enable natural keys. Thus the
  full command becomes: `python manage.py dumpdata --format yaml--natural-foreign --natural-primary myapp`.
  This avoids a problem with generic relations: Each model with a generic relation must have a foreign
  key on the `ContentType` model that contains a list of all known models. This uses an auto-incremented
  ID that is not stable. Without natural keys the fixtures would contain the raw ID of the content type,
  that would most-likely not reference the model we want during import of the fixture.

* **Load Initial Data:** Once your new fixture is working, consider adding it to the `load_initial_data`
  management command. The source code is in the `lernspiel_server` project directory. This allows other
  developers and users to import a complete set of initial data with only one command.

**Natural keys, part II:** Why are we not using natural keys for our models? After writing the lines
above the initial plan was to add natural keys to all own models, so that the fixtures would be free
from UUIDs and generally much easier to read. But the attached trade-offs quickly outgrew the benefit:

* Adding natural keys to each model increases the size considerably: `natural_key()` method, custom
  manager, unique constraint for each model. But that alone would have been okay, as we didn't want
  to introduce a dependency to [Django Natural Keys](https://pypi.org/project/natural-keys/) to keep
  the dependencies minimal.

* Many models have a name, that would be a perfect fit for the natural key. But it might be problematic
  to make them unique.

* Generic relations are still problematic due to the `object_id` property. That was the real killer.
  Why all the effort, if each generic relation still references the UUID of the related object?
  For this to work the UUID of the related object must be enforced during import, neglecting the reason
  to add natural keys in the first place.

  There is a work-around using [custom serializers and deserializers](https://stackoverflow.com/a/70700302).
  But that is quite a lot of code that needs deep understanding of Django's inner workings. 🤯
  Clearly something to avoid, if at all possible.

Thankfuly using UUIDs the problem is not as large as if we were using the traditional auto-incremented
IDs. With auto-incremented IDs natural keys are needed to ensure stable keys. Otherwise entries will
not be imported if the ID is already used by another entry and imported foreign keys will reference
the wrong object. UUIDs are supposed to be globally unique by default, avoiding most of the problems
in the first place.

SQLite Shell
------------

The command `./manage.py dbshell?` drops you into a database shell where you can execute SQL
commands against the database. Unfortunately the SQLite shell typically used during development
is very spartan. The `SELECT` output doesn't even show the column names. The following special
commands mitigate this a litte:

* `.tables` - List available tables
* `.mode column` - Turn column mode on to align the SELECT output in columns
* `.headers on` - Show column names in the first line
* `.quit` - Leave SQLite Shell (and use a proper tool 😛)

Make sure to use an extra wide terminal window, as the lines are still unreadebl when wrapped.

NPM and esbuild
---------------

Lernspiel Online uses a mixture of traditional server-side rendering and more modern client-side rendering.
Server-side rendering using Django views and templates is used for all static and non-game pages. Client-side
rendering is used for the games, using a websocket connection to the server to allow real-time communication
between players, teacher and server. All in all, we still try to keep the code as simple as possible, tending
to avoid complex libraries.

On the other hand, the NPM package index has be come a very convenient de-facto standard not only
for Node.js server-side libraries but also for client-side libraries. We therefor use a subset of
Node.js and NPM to pull client-side libraries and bundle them into distribution files with
[esbuild](https://esbuild.github.io/).

The root-level [package.json](package.json) defines a NPM workspace, so that all NPM projects share
a global `node_modules` directory. It also defines most build-tools via its `devDependencies`, so
that they need not be maintained in several locations. Besides that, each sub-project has its own
`package.json` for runtime dependencies, additional development dependencies and run scripts. Typical
run scripts are:

* `npm run build` - Build distribution files
* `npm run clean` - Delete distribution files
* `npm run watch` - Start watch mode for automatical rebuilds
* `npm run check` - Run all checks and tests: eslint, TypeScript, unit tests
* `npm run start` or `npm start` - Run from built distribution files

Less-often used commands:

* `npm run test` - Run unit tests only
* `npm run tsc` - Check source code with TypeScript only
* `npm run lint` - Check source code with eslint only
* `npm run lintfix` - Auto-correct eslint findings (be careful!)
* `npm run prettier` - Check source code formatting with prettier
* `npm run format` - Auto-correct prettier findings (be careful!)


The Game Server Data Model
--------------------------

Here's a quick overview of how the game data model is organized:

### Almost Everything is a Game Component

Games are made up of nested game components. Much like HTML pages are made up
of nested HTML elements (or custom web components). Unlike HTML however, a game
component combines rendering logic and game logic, which are executed on the client
and server side respectively. Also a game component can have more than one "slot"
for child components.

Besides that there is no restriction of what a game component can be. Some components
render a nice frame around the actual game, others render questions, title cards,
player lists, HTML text, high scores, ... or simply manage the game state. Game designers
can mix and match the components and extend them with custom logic to build their games.

### The Holy Trinity of Meta, Definition and Runtime

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


Developing New Game Components
------------------------------

TODO - The Game SDK will be used for this.
