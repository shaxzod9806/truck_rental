from django.urls import path
from . import views

urlpatterns = [
    path('brands/', views.BrandAPI.as_view(), name="equipment_brand"),
    path('brands/<int:pk>', views.SingleBrandAPI.as_view(), name="single_brand"),
    path('category/', views.CategoryAPI.as_view(), name="equipment_category"),
    path("categoryList/", views.CategoryList.as_view(), name="categoryLst"),
    path("categoryGetOne/<int:pk>/", views.CategoryGetOne.as_view(), name="category_get_one"),
    path('category/<int:pk>', views.SingleCategory.as_view(), name="single_category"),
    path('sub_category', views.SubCatApi.as_view(), name="sub_category"),
    path('sub_category/<int:pk>', views.SingleSubCategory.as_view(), name="single_sub_cat"),
    path("sub_categoryList/", views.SubCategoryList.as_view(), name="sub_category_list"),
    path("sub_categoryGetOne/<int:pk>/", views.SubCategoryGetOne.as_view(), name="category_get_one"),
    path('equipment/', views.EquipmentAPI.as_view(), name="equipment_api"),
    path('equipment/<int:pk>', views.SingleEquipment.as_view(), name="single_equipment"),
    path("equipmentList/", views.EquipmentList.as_view(), name="equipmentLst"),
    path("equipmentGetOne/<int:pk>/", views.EquipmentGetOne.as_view(), name="equipmentLst_get_one"),
    path('additions/', views.AdditionsApi.as_view(), name="additions"),
    path('additions/<int:pk>', views.SingleAddition.as_view(), name="addition_single"),
    path('additions_of_equipment/<int:pk>', views.SingleEquipmentAdditions.as_view(),
         name="additions_equipment_single"),
]
