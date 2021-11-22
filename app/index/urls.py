from . import views
from django.urls import path, include

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.UserRegister.as_view(), name="register_user")
]
