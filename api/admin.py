from django.contrib import admin
from api.models import Property, PropertyType, Status

# Register your models here.
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(Status)
