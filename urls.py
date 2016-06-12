from django.conf.urls import url

from . import views

urlpatterns = [
    url (   r'^$',
            views.ItemList.as_view(),
            name="index",
        ),

    url (   r'^$',
            views.ItemList.as_view(),
            name="item_list",
        ),

    url (   r'^locations/$',
            views.LocationList.as_view(),
            name="location_list",
        ),

    url (   r'^locations/new/$',
            views.LocationCreate.as_view(),
            name="location_create",
        ),
]
