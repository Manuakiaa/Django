from decouple import config


SECRET_KEY = config("GAMERLAIR_SECRET_KEY", cast=str)
ENV_ID = config("GAMERLAIR_ENV_ID", cast=str)
