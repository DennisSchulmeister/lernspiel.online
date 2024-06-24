Developer Notes for Lernspiel Online
==========================

This document serves as a cheat sheet for developers to get started quickly. There are no
fancy things -- if you already know Python, Poetry, Django, NPM, … But finding the right
information might not be easy when working with so much different technology. This document
tries to summarize the most important things.

1. [Technology Choices](#technology-choices)
1. [Directory Layout](#directory-layout)
1. [Poetry Package Management](#poetry-package-management)
1. [Django Web Framework](#django-web-framework)
1. [Django Project vs. App](#django-project-vs-app)
1. [SQLite Shell](#sqlite-shell)
1. [NPM and esbuild](#npm-and-esbuild)
1. [Developing New Game Variants](#developing-new-game-variants)

Technology Choices
------------------

Lernspiel Online is built with the following technology:

* Python
* Django Web Framework - Core Technology
* Django Channels - Websocket Support
* Poetry - Package Management

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
│   ├── cli                             Game SDK CLI
│   └── web                             Game SDK Client Library
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

The only thing we find unfortunate is, that apps by default live outside their parent project.
This makes sense for reusable apps, that are meant to be used in multiple projects. But for
internal apps this clutters the source directory, making it hard for administrators to find
the settings file and other important directories. It also allows naming clashes with globally
installed Python packages. For this reasons we put the internal apps of a project **inside**
the projects module directory. (And still the so called app name can clash, since Django by
default only uses the last part of the package name for it.)

Take the `lernspiel_server` project and its internal `pages` app. Instead of:

```text
.
├── HACKING.md
└── lernspiel_server
    ├── pages
    │   └── ...
    ├── lernspiel_server
    │   ├── local_settings.py
    │   ├── settings.py
    │   └── ...
    └── manage.py
```

We have:

```text
.
├── HACKING.md
└── lernspiel_server
    ├── lernspiel_server
    │   ├── pages
    │   │   └── ...
    │   ├── local_settings.py
    │   ├── settings.py
    │   └── ...
    └── manage.py
```

For this first create an app as usual with:

```sh
./manage.py startapp myapp
```

Then move the new app directory into the project's python module directory (e.g. `myproject`).
The new app name with thus become `myproject.myapp`, which needs to be reflected in the `name`
attribute inside the `apps.py` file. Otherwise Django bails on server startup. When adding the
app to the `INSTALLED_APPS` settings also use the new name `myproject.myapp`.

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

Developing New Game Variants
----------------------------

TODO - The Game SDK will be used for this.
