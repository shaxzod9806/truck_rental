from django.shortcuts import render
from .models import Order, OrderChecking
from index.models import User
from customer.models import CustomerProfile
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from utilities.mapping import find_near_equipment
from datetime import datetime
from equipments.models import Equipment
from renter.models import Profile as renter_profile
from renter.models import RenterProduct
from datetime import timedelta
from utilities.models import SMS
from utilities.sms import send_sms
from utilities.mapping import send_confirm_sms


# Create your views here.


class OrderAPIView(APIView):
    permission_class = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = OrderSerializer

    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(request_body=OrderSerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def post(self, request):
        serializer = OrderSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            near_equipment = find_near_equipment(float(data["lat"]), float(data["long"]))
            checking_order = OrderChecking.objects.create(
                renter=User.objects.get(id=near_equipment["renter_id"]),
                equipment=RenterProduct.objects.get(id=near_equipment["product_id"]),
                order=Order.objects.get(id=data["id"]),
                confirmed=1,
                checking_end=datetime.today()
            )
            checking_order.checking_end = checking_order.checking_start + timedelta(minutes=15)
            checking_order.save()
            # Notify the user
            renter = renter_profile.objects.get(id=near_equipment["renter_id"])
            send_confirm_sms(renter, SMS)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order_id = openapi.Parameter(
        'order_id', in_=openapi.IN_FORM,
        description='enter order ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(request_body=OrderSerializer, parser_classes=parser_classes,
                         manual_parameters=[order_id, param_config])
    def put(self, request):
        customer_id = request.data["customer"]
        customer = CustomerProfile.get(id=customer_id)
        user_type = customer.user.user_type
        if user_type <= 2:
            order_id = request.data["order_id"]
            order = Order.objects.get(id=int(order_id))
            serializer = OrderSerializer(order, many=False, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("not accessible for customer and user", status=status.HTTP_400)

    @swagger_auto_schema(manual_parameters=[order_id, param_config])
    def delete(self, request):
        customer_id = request.data["customer"]
        customer = CustomerProfile.get(id=customer_id)
        user_type = customer.user.user_type
        if user_type <= 2:
            try:
                order = Order.objects.get(id=int(request.data['order_id']))
                order.delete()
                return Response({'detail': 'Order is deleted'}, status=status.HTTP_200_OK)
            except:
                return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("not accessible customer and user", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleOrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    parser_classes = (MultiPartParser, FormParser)

    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes)
    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelAPI(APIView):
    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    order_id = openapi.Parameter(
        'order_id',
        in_=openapi.IN_QUERY,
        description='Enter order id ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[order_id, token])
    def post(self, request):
        order_id = request.GET.get('order_id')
        print(order_id)
        order_itself = Order.objects.get(id=order_id)
        if not order_itself.renter:
            order_itself.user_cancel = True
            return Response({"details": "order canceled"}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "there is already connected renter"}, status=status.HTTP_400_BAD_REQUEST)
