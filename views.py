from django.shortcuts import render
from django.views import generic

from .models import Location, Item

class ItemList(generic.ListView):
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).order_by("id")
