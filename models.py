from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name        = models.CharField(max_length=20)
    comment     = models.CharField(max_length=40)
    parent      = models.ForeignKey('self', default=None, null=True)
    owner       = models.ForeignKey(User)
    last_mod    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%d)" % (self.name, self.id)

class Item(models.Model):
    name        = models.CharField(max_length=20)
    item_type   = models.CharField(max_length=20)
    comment     = models.CharField(max_length=40)
    location    = models.ForeignKey(Location)
    owner       = models.ForeignKey(User)
    last_mod    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s) #%d" % (self.name, self.item_type, self.id)