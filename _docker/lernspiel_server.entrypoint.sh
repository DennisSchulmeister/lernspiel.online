#! /bin/sh

# NOTE: The server is started using exec to replace the shell process with the new process.
# This makes sure that the process receives the operating signals generated by Docker, especially
# SIGTERM, when the container is being stopped. See :https://unix.stackexchange.com/a/196053

if [ -n "$1" ]; then
    echo ">>> Starting worker process: $1 <<<"
    exec ../.env/bin/python ./manage.py runworker "$1"
else
    echo ">>> Starting lernspiel-server <<<"

    mkdir -p _static
    cp -r _static/* _static.volume

    ../.env/bin/python ./manage.py migrate

    if [ -n "$LS_LOAD_INITIAL_DATA" ]; then
        ../.env/bin/python ./manage.py load_initial_data
    fi

    exec ../.env/bin/daphne -p 8000 -b 0.0.0.0 lernspiel_server.asgi:application
fi