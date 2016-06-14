from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
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
class LocationDetail(generic.DetailView):
    def get_queryset(self):
        return Location.objects.filter(id=self.kwargs['pk'],
                                    owner=self.request.user)

@method_decorator(decs, name='dispatch')
class LocationCreate(generic.edit.CreateView):
    model       = Location
    success_url = reverse_lazy("consus:location_list")
    fields      = ["name", "comment", "parent", ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(LocationCreate, self).form_valid(form)


@method_decorator(decs, name='dispatch')
class LocationEdit(generic.UpdateView):
    model       = Location
    fields      = ["name", "comment", "parent", ]
    template_name = "consus/location_edit.html"

    def get_success_url(self):
        return reverse("consus:location_detail", args=[self.object.id])


@method_decorator(decs, name='dispatch')
class ItemList(generic.ListView):
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).order_by("id")

@method_decorator(decs, name='dispatch')
class ItemCreate(generic.edit.CreateView):
    model       = Item
    success_url = reverse_lazy("consus:item_list")
    fields      = ["name", "item_type", "location", "comment", ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ItemCreate, self).form_valid(form)
