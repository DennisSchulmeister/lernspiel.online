Installation Notes for Administrators
=====================================

1. [Local Settings](#local-settings)
1. [Web Server](#web-server)
1. [Docker Compose](#docker-compose)

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

In the good old WSGI days Apache + mod_python used to be a reliable way to server Django applications.
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
* `webserver` (container `docker-webserver-1`): Frontend webserver

As of today there is no official docker image on Docker Hub. Therefor the directory contains a
Dockerfile that will be built on demand. For the time being the recommendation is to pull the
source code from GitHub, copy the `_docker` directory to a new location outside the git tree
and adapt it to your needs.

Get in touch with us, if you like to work on an official Docker image, once the platform is
sufficiently mature enough.