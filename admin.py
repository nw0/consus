from django.contrib import admin

from .models import Location, Item

admin.site.register(Location)
admin.site.register(Item)

def other_checks(user):
    return user.groups.filter(name="Consus Users")
