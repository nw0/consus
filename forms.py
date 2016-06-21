from django import forms

from .models import Location, Item

class LocationForm(forms.ModelForm):
    name    = forms.CharField(max_length=20)
    name.widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model   = Location
        fields  = ["name", "comment", "parent", ]

class ItemForm(forms.ModelForm):
    name    = forms.CharField(max_length=20)
    name.widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model   = Item
        fields  = ["name", "item_type", "location", "comment", ]
