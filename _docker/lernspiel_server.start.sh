#! /bin/sh

echo "Starting lernspiel-server"
echo "========================="
echo

mkdir -p _static
cp -r _static/* _static.volume

../.env/bin/daphne -p 8000 -b 0.0.0.0 lernspiel_server.asgi:application