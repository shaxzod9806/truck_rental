from . import views
from django.urls import path

urlpatterns = [
    path('SecondRegistration_userID_API/', views.SecondRegistration_userID_API.as_view(),
         name='SecondRegistrati_userID_API'),
    path('SecondRegistrationAPI/', views.SecondRegistrationAPI.as_view(), name='SecondRegistrationAPI'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('device_id/', views.Device_idView.as_view(), name='Device_idView'),
    path('register/', views.UserRegister.as_view(), name="register_user"),
    path("verify_user/", views.VerifyUser.as_view(), name="verify_user"),
    path("1_reset_phone_number/", views.ResetPhoneNumber.as_view(), name='reset_phone_number'),
    path("2_ResetVerifyUserCode/", views.ResetVerifyUserCode.as_view(), name='reset_verify_user_code'),
    path('3_Reset_New_Password/', views.Reset_New_Password.as_view(), name='reset_new_password'),
    path("user_edit/", views.UserEditAPI.as_view(), name='user_edit')
]
