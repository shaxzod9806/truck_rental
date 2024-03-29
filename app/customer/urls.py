from django.urls import path
from .views import CustomerProfileAPI, CustomerRegisterAPI, RegionAPI, CountryAPI,SingleCustomerAPI,Profil_Editing_API

urlpatterns = [
    path('customer_profile', CustomerProfileAPI.as_view(), name="get_customer_profile"),
    path('customer_profile_edit', Profil_Editing_API.as_view(), name="get_customer_profile_edit"),
    path('customer_profile_one', SingleCustomerAPI.as_view(), name="get_one_customer_profile"),
    path('customer_register', CustomerRegisterAPI.as_view(), name="customer_register"),
    path('country', CountryAPI.as_view(), name="country"),
    path('region', RegionAPI.as_view(), name="region"),
]
