from django.urls import path
from . import views

urlpatterns = [
    path("order/",views.OrderApi.as_view(),name="order")
]