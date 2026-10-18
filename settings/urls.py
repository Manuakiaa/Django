from decouple import config

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path(config("GAMERLAIR_ADMIN_URL", cast=str), admin.site.urls),
]
