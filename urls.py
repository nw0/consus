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

    url (   r'^items/new/$',
            views.ItemCreate.as_view(),
            name="item_create",
        ),

    url (   r'^items/(?P<pk>\d+)/edit/$',
            views.ItemEdit.as_view(),
            name="item_edit",
        ),

    url (   r'^locations/$',
            views.LocationList.as_view(),
            name="location_list",
        ),

    url (   r'^locations/(?P<pk>\d+)/$',
            views.LocationDetail.as_view(),
            name="location_detail",
        ),

    url (   r'^locations/new/$',
            views.LocationCreate.as_view(),
            name="location_create",
        ),

    url (   r'^locations/(?P<pk>\d+)/edit/$',
            views.LocationEdit.as_view(),
            name="location_edit",
        ),
]
