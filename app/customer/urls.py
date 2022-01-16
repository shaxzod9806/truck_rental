from django.urls import path
from .views import CustomerProfileAPI, CustomerRegisterAPI

urlpatterns = [
    path('customer_profile', CustomerProfileAPI.as_view(), name="get_customer_profile"),
    path('customer_register', CustomerRegisterAPI.as_view(), name="customer_register"),
]
