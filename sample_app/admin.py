
from django.contrib import admin
from .models import *
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.sessions.models import Session


app_models = apps.get_app_config('sample_app').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

admin.site.register(Session)


