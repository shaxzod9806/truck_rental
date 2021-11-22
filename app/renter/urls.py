from . import views
from django.urls import path, include

urlpatterns = [
    path('user_profile', views.UserProfile.as_view(), name="get_user_profile"),
    path('register_profile', views.ProfileRegister.as_view(), name="register_profile"),
]
