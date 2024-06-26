# Deployment-specific local settings
# ----------------------------------
#
# This is an example configuration for the Lernspiel Online server used by the example
# Docker Compose setup. The original file from which this was derived lives in the source
# tree of the Lernspiel Online server. See the comments there for details.

# Replace with your own secret key !!
SECRET_KEY = "django-insecure-l2i@-07@^2yju3jy_j(o4*41l=yl^tf@k5hq9u$uz-#kw-88&j"
DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lernspiel",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": "5432",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATIC_DIR = "/app/lernspiel_server/_static.volume"
STATIC_URL = "static/"

MEDIA_DIR = "/app/lernspiel_server/_media.volume"
MEDIA_URL = "media/"

USE_TZ = True
TIME_ZONE = "Europe/Berlin"

LANGUAGE_CODE = "de-de"
USE_THOUSAND_SEPARATOR = True

SITE_ID = 1