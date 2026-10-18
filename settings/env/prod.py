from decouple import config

from settings.base import *  # noqa


DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("GAMERLAIR_POSTGRES_DB", cast=str),
        "USER": config("GAMERLAIR_POSTGRES_USER", cast=str),
        "PASSWORD": config("GAMERLAIR_POSTGRES_PASSWORD", cast=str),
        "HOST": config("GAMERLAIR_POSTGRES_HOST", cast=str),
        "PORT": config("GAMERLAIR_POSTGRES_PORT", cast=int),
    }
}
