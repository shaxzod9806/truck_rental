from django.urls import path
from . import views
urlpatterns = [
    path('category/', views.CategoryAPI.as_view(), name="equipment_category"),
    path('category/<int:pk>', views.SingleCategory.as_view(), name="single_category"),
    path('sub_category', views.SubCatApi.as_view(), name="sub_category"),
    path('sub_category/<int:pk>', views.SingleSubCategory.as_view(), name="single_sub_cat"),
    path('equipment/', views.EquipmentAPI.as_view(), name="equipment_api"),
    path('equipment/<int:pk>', views.SingleEquipment.as_view(), name="single_equipment"),
    path('additions/', views.AdditionsApi.as_view(), name="additions"),
    path('additions/<int:pk>', views.SingleAddition.as_view(), name="addition_single"),
]