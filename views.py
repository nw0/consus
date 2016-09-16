from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import generic

import json

from .admin import other_checks
from .forms import LocationForm, ItemForm
from .models import Location, Item

decs = [ login_required, user_passes_test(other_checks), ]

@method_decorator(decs, name='dispatch')
class LocationList(generic.ListView):
    def get_queryset(self):
        return Location.objects.filter(owner=self.request.user).order_by("id")

def extract_locations(locs, get_items=False):
    ans = []
    for loc in locs:
        child_items = []
        if get_items:
            for item in loc.item_set.all():
                child_items.append({"name": item.name})
        child_locs = extract_locations( Location.objects.filter(parent=loc),
                                        get_items)
        ans.append({"name": loc.name,
                    "is_location": True,
                    "children": child_items + child_locs})
    return ans

def dump_item(it):
    return {
        'name': it.name,
        'item_type': it.item_type,
        'comment': it.comment,
    }

def dump_loc(loc):
    return {
        'name': str(loc.name),
        'comment': str(loc.comment),
        'sublocs': [dump_loc(sl) for sl in Location.objects.filter(parent=loc)],
        'items': [dump_item(i) for i in Item.objects.filter(location=loc)],
    }

@login_required
@user_passes_test(other_checks)
def export_data(request):
    loc_list = list(Location.objects.filter(owner=request.user, parent=None))
    ans = []
    for loc in loc_list:
        ans.append(dump_loc(loc))
    return HttpResponse(json.dumps(ans))

@login_required
@user_passes_test(other_checks)
def LocationListJSON(request):
    loc_list = Location.objects.filter(owner=request.user, parent=None)
    ans = { "name": "locations",
            "is_root": True,
            "children": extract_locations(loc_list, True)}
    return HttpResponse(json.dumps(ans))

@login_required
@user_passes_test(other_checks)
def LocationTree(request):
    template = loader.get_template("consus/location_tree.html")
    return HttpResponse(template.render({}, request))

@method_decorator(decs, name='dispatch')
class LocationDetail(generic.DetailView):
    def get_queryset(self):
        return Location.objects.filter(id=self.kwargs['pk'],
                                    owner=self.request.user)

@method_decorator(decs, name='dispatch')
class LocationCreate(generic.edit.CreateView):
    model       = Location
    form_class  = LocationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(LocationCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("consus:location_detail", args=[self.object.id])


@method_decorator(decs, name='dispatch')
class LocationEdit(generic.UpdateView):
    model       = Location
    form_class  = LocationForm
    template_name = "consus/location_edit.html"

    def form_valid(self, form):
        if form.instance.owner != self.request.user:
            raise ValidationError("Wrong owner")
        #   Check for loops
        return super(LocationEdit, self).form_valid(form)

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
    form_class  = ItemForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ItemCreate, self).form_valid(form)

@method_decorator(decs, name='dispatch')
class ItemEdit(generic.UpdateView):
    model       = Item
    success_url = reverse_lazy("consus:item_list")
    form_class  = ItemForm
    template_name = "consus/item_edit.html"

    def form_valid(self, form):
        if form.instance.owner != self.request.user:
            raise ValidationError("Wrong user")
        return super(ItemEdit, self).form_valid(form)
