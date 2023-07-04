from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

from django.apps import apps

for model in apps.get_app_config('myapp').models.values():
    admin.site.register(model)
