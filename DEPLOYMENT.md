Installation Notes for Administrators
=====================================

1. [System Overview](#system-overview)
1. [Local Settings](#local-settings)
1. [Web Server](#web-server)
1. [Game Runners](#game-runners)
1. [Docker Compose](#docker-compose)

System Overview
---------------

Regarding deployment this is a pretty standard Django project. Please see the
[Django Documentation](https://docs.djangoproject.com/en/5.0/#the-development-process)
for all details. Below is a quick summary including a few notable considerations.

![Deployment Architecture](_img/deployment-architecture.png)

* __Front Webserver:__ This is not strictly necessary but usually you want one for
  the following tasks:

   * TLS termination
   * Serving of static files
   * Serving of uploaded media files
   * Reverse proxy to the application

  The last part is kind-of optional, if you have multiple domains like https://example.com,
  https://static.example.com and https://media.example.com pointing to different machines.
  A more basic setup hosts everything on one machine and uses the front webserver to host
  static and media files and forward all other requests to the Django application.

  Almost any production webserver will do. For many people, [Apache http](https://httpd.apache.org)
  is the battle-proven de-facto standard. But [Caddy](https://caddyserver.com/) is a nice and
  modern alternative with very little configuration.

* __Lernspiel Server:__ The Lernspiel server really consists of two parts: A stock ASGI server
  like [Daphne](https://github.com/django/daphne) to run the Django application and at least
  one _Game Runner Process_ to execute the server-side game logic. This sounds complicated but
  is nothing more than a basic [Django Channels Deployment](https://channels.readthedocs.io/en/stable/deploying.html)
  with one [background worker](https://channels.readthedocs.io/en/stable/topics/worker.html).

  Daphne is already a dependency anyhow, so in practice this simply means:

  1. Start Daphne server: `daphne -p 8000 -b 0.0.0.0 lernspiel_server.asgi:application`
  2. Start Game Runner: `./manage.py runworker game-runner`

* __Redis:__ Since we are using Django Channels for websocket support and inter-process communication
  a [Channel Layer](https://channels.readthedocs.io/en/stable/topics/channel_layers.html) must be set-up.
  The pre-configured default option is to use [Redis](https://redis.io/) for this. The default configuration
  expects the Redis server to listen to `localhost:6379` but this setting can be overwritten in the local
  settings file.

* __Database:__ A database like [MariaDB](https://mariadb.org/) or [Postgres](https://www.postgresql.org/)
  is needed for persistent storage. See the [Django Documentation](https://docs.djangoproject.com/en/5.0/ref/databases/)
  for all supported databases. Make sure to pip install the correct database driver and adopt the local
  settings file accordingly.

See the provided Docker and Docker Compose files for a working example. Also note, that despite the image,
all components are scalable by default. If your front server can load balance to multiple backends, you
can easily start multiple backend instances, multiple game runners etc. to fully utilize the hardware.
It is up to you whether to distribute the components to individual machines/VMs/containers or not. But
even a basic setup on one machine can go very far. To keep things simple we recommend to start small and
only scale-up when the need becomes real.

Local Settings
--------------

Settings is probably the one part of Django where you really feel its old age. By default there is
no way standard way to separate local deployment-specific settings (e.g. database credentials) from
local development settings. We are using a simple approach here:

* File `settings.py`: Contains the base settings, plus everything needed for local development.
* File `local_settings.py`: Specific settings for deployment or a special local setup.

The file `local_settings.py` is therefor excluded from version control. There is a template file
that explains some settings that you usually want to override.

Web Server
----------

In the good old WSGI days Apache + mod_python used to be a reliable way to serve Django applications.
Since this project also uses Django Channels for websocket support, we need an ASGI-capable server, instead.
Django Channels already comes with the Daphne server. You can run it like this:

```sh
cd lernspiel_server
daphne -p 8000 -b 0.0.0.0 lernspiel_server.asgi:application
```

On your local development machine you might need to use `poetry run` to run Daphne from within the
Python environment.

When running behind a reverse proxy (e.g. because you host multiple apps and/or sites on the same
machine), you usually want to bind to localhost only:

```sh
cd lernspiel_server
daphne -p 8000 lernspiel_server.asgi:application
```

If you are still looking for a good reverse proxy (or webserver in general), try out [Caddy](https://caddyserver.com/).
Its configuration is much, much simpler than Apache and it works at least as reliable. Websocket connections
are easily proxied without extra configuration and SSL certificate renewal with Let's Encrypt is fully automated.
Give it a try.

Oh, and don't forget to serve static and uploaded media files. By default they live in the `_static/` and
`_media/` directories of each Django project. But you can override the filesystem path and the final web
URL in your `local_settings.py`. Once that is done you need to "collect" the static files with the following
command:

```sh
python ./manage.py collectstatic
```

Game Runners
------------

Execution of the game logic is separate from the HTTP worker processes, to decouple the game state from the
player connections. This allows games to have a server-side global state that can be updated "in background"
no matter which participant is currently connected with the server. In practice this means:

* At least one game runner process must be running in parallel to the ASGI server.
* [Redis](https://redis.io/) or any other channel layer backend must be setup.

The default option to connect multiple processes in the Django Channels world is Redis. This is the pre-defined
default option for the Lernspiel Server, too, during development and in production. Once this is running, the
game runner processes can be started like this:

```sh
cd lernspiel_server
python manage.py runworker game-runner
```


Docker Compose
--------------

The [_docker](_docker) directory contains a working example configuration for Docker Compose.
You can use it to test a full deployment build on your local machine and as a template for your
own deployment. The following commands will be helpful:

* `docker compose build` - Build docker images
* `docker compose up` - Start all services in foreground (end with CTRL+C)
* `docker compose up -d` - Start all services in background
* `docker compose down` - Stop all services, either in foreground or background
* `docker exec -it docker-lernspiel-server-1 sh` - Open a shell on the lernspiel server

The following services are defined:

* `postgres` (container `docker-postgres-1`): Persistent database
* `redis` (container `docker-redis-1`): Key/value store for asynchronous processes
* `lernspiel-server` (container `docker-lernspiel-server-1`): The main server
* `game-runner` (containers `game-runner-1` and `game-runner-2`): Two game runner processes
* `webserver` (container `docker-webserver-1`): Frontend webserver

As of today there is no official docker image on Docker Hub. Therefor the directory contains a
Dockerfile that will be built on demand. For the time being the recommendation is to pull the
source code from GitHub, copy the `_docker` directory to a new location outside the git tree
and adapt it to your needs.

Get in touch with us, if you like to work on an official Docker image, once the platform is
sufficiently mature enough.