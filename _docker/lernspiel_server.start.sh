#! /bin/sh

echo "Starting lernspiel-server"
echo "========================="
echo

mkdir -p _static
cp -r _static/* _static.volume

../.env/bin/python ./manage.py migrate

# TODO: Find better solution
../.env/bin/python ./manage.py load_initial_data

../.env/bin/daphne -p 8000 -b 0.0.0.0 lernspiel_server.asgi:application