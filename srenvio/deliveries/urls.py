from django.urls import path

from django.conf.urls import url, include
from .views import DeliveryList

urlpatterns = [
    path("", DeliveryList.as_view(), name="delivery-list"),
   
]
