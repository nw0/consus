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
]
