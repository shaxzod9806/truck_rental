from django.urls import path
from . import views

urlpatterns = [
    path('register_manager', views.RegisterManagerAPIView.as_view(), name='register_manager'),
    path('manager', views.ManagerAPIView.as_view(), name='manager'),
    path('manager_one', views.SingleManagerAPIView.as_view(), name='single_manager'),
]
