from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic

from .admin import other_checks
from .models import Location, Item

decs = [ login_required, user_passes_test(other_checks), ]

@method_decorator(decs, name='dispatch')
class LocationList(generic.ListView):
    def get_queryset(self):
        return Location.objects.filter(owner=self.request.user).order_by("id")

@method_decorator(decs, name='dispatch')
class ItemList(generic.ListView):
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).order_by("id")
