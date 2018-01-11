from django.contrib import admin
from api.models import Owner, Property, PropertyType, Status

# Register your models here.
admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(Status)