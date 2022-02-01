from . import views
from django.urls import path, include

urlpatterns = [
    path('user_profile', views.UserProfile.as_view(), name="get_user_profile"),
    path("renter_order/", views.RenterOrdersAPI.as_view(), name="renter_order"),

    # path('files'  , views.FileAPI.as_view(), name="files"),
    # path('files/<int:pk>', views.SingleFileAPIView.as_view(), name="single_file"),
    path('register_profile', views.ProfileRegister.as_view(), name="register_profile"),
    path('RentrProduct/', views.RentrProductAPI.as_view(), name="RentrProduct"),
    path('RentrProduct/<int:pk>/', views.SingleRentrProductAPI.as_view(), name="RentrProduct_id"),
]
