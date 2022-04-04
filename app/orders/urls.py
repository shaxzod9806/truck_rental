from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.OrderAPIView.as_view(), name="order"),
    path('order/<int:pk>', views.SingleOrderAPI.as_view(), name="single_order"),
    path("order_cancel_api/", views.OrderCancelAPI.as_view(), name="order_cancel_api"),
    path("order_accept_api/", views.OrderAcceptAPI.as_view(), name="order_accept_api"),
    path('RefreshFireBaseTokenView/', views.RefreshFireBaseTokenView.as_view(), name="RefreshFireBaseTokenView"),
    path('FireBaseView/', views.FireBaseView.as_view(), name="FireBaseView"),
]
