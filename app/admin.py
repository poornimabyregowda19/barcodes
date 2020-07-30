
# Register your models here.
from django.contrib import admin

# Register your models here.
from django.apps import apps
myapp = apps.get_app_config('app')

for key, value in myapp.models.items():
    admin.site.register(value)