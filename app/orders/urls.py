from django.urls import path
from . import views

urlpatterns = [
    path("order/",views.OrderAPIView.as_view(),name="order")
]