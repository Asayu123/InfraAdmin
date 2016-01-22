from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.apps import apps  # import this for Automatic Model Registration.

from . import models

# Register your models here.

# WARNING: This iteration will include hidden table: ex, relationship table for ManytoMany Field.
myApp = apps.get_app_config('ServerAdmin')  # Automatically Register All models in this app.
modelSet = myApp.models.values()

for model in modelSet:
    admin.site.register(model,ImportExportModelAdmin)
