#===============================================================================
# Build container
#===============================================================================
FROM python:slim AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN python -m venv .env
RUN .env/bin/pip install poetry poetry-plugin-export
RUN .env/bin/poetry export --format=requirements.txt --output=requirements.txt

#===============================================================================
# App container
#===============================================================================
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p lernspiel_server/_static.volume
RUN mkdir -p lernspiel_server/_media.volume

COPY --from=build /app/requirements.txt . 
RUN python -m venv .env
RUN .env/bin/pip install -r requirements.txt
RUN .env/bin/pip install psycopg

COPY . .
COPY _docker/lernspiel_server.start.sh lernspiel_server/start.sh
RUN chmod +x lernspiel_server/start.sh

# This copies to _static, according to settings.py
RUN .env/bin/python lernspiel_server/manage.py collectstatic --noinput

VOLUME /app/lernspiel_server/_media.volume
VOLUME /app/lernspiel_server/_static.volume
EXPOSE 8000

WORKDIR /app/lernspiel_server
CMD ["./start.sh"]
