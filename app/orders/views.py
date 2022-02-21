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
from utilities.sms import send_confirm_sms
from utilities.price_calculation import renting_time_calc
from equipments.views import BasicPagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from utilities.pagination import PaginationHandlerMixin
from django.utils.dateparse import parse_datetime


# Create your views here.


class OrderAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
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
        serializer = OrderSerializer(data=request.data, many=False, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            near_equipment = find_near_equipment(float(data["lat"]), float(data["long"]))
            profile_renter = renter_profile.objects.get(id=near_equipment["renter_id"])
            order_itself = Order.objects.get(id=data["id"])
            checking_order = OrderChecking.objects.create(
                renter=profile_renter.user,
                equipment=RenterProduct.objects.get(id=near_equipment["product_id"]),
                order=order_itself,
                confirmed=1,
                checking_end=datetime.today()
            )
            checking_order.checking_end = checking_order.checking_start + timedelta(minutes=15)
            checking_order.save()
            # Notify the user
            renter = renter_profile.objects.get(id=near_equipment["renter_id"])
            #  This should be function outside of view
            start_time = data["start_time"]
            end_time = data["end_time"]
            renting_time = renting_time_calc(start_time, end_time)
            total_price = order_itself.equipment.hourly_price * renting_time
            address = order_itself.address
            data["order_price"] = total_price
            data["notes"] = data["notes"]
            data["renter"] = renter.id
            orderjon = Order.objects.get(id=data["id"])
            orderjon.start_time = parse_datetime(start_time)
            orderjon.end_time = parse_datetime(end_time)
            send_confirm_sms(renter, SMS, start_time, end_time, total_price, address)
            return Response(data, status=status.HTTP_200_OK)
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
            serializer = OrderSerializer(order, many=False, data=request.data, context={"request": request})
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

    ordering = openapi.Parameter(
        'ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description='Enter field name to order for example: "cat_name" ascending; '
                    'put "-" for reverse ordering: "-cat_name"'
    )

    @swagger_auto_schema(manual_parameters=[param_config, ordering])
    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        page = self.paginate_queryset(orders)
        serializer = OrderSerializer(page, many=True, context={"request": request})
        if page is not None:
            serializer = self.get_paginated_response(
                OrderSerializer(page, many=True, context={"request": request}).data)
        else:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True, context={"request": request}).data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SingleOrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    parser_classes = (MultiPartParser, FormParser)

    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes)
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order, many=False, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderCancelAPI(APIView):
    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    order_id = openapi.Parameter(
        'order_id',
        in_=openapi.IN_FORM,
        description='Enter order id ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[order_id, token])
    def post(self, request):
        order_id = request.GET.get('order_id')
        order_itself = Order.objects.get(id=order_id)
        if not order_itself.renter:
            order_itself.user_cancel = True
            return Response({"details": "order canceled"}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "there is already connected renter"}, status=status.HTTP_400_BAD_REQUEST)


class OrderAcceptAPI(APIView):
    permission_classes = [IsAuthenticated]
    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )
    order_id = openapi.Parameter(
        'order_id',
        in_=openapi.IN_QUERY,
        description='Enter order id',
        type=openapi.TYPE_INTEGER
    )

    is_accept = openapi.Parameter(
        'is_accept',
        in_=openapi.IN_QUERY,
        description='2-cancel;  3-accept',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[order_id, token, is_accept])
    def post(self, request):
        order_id = request.GET.get('order_id')
        is_accept = request.GET.get('is_accept')
        renter = request.user
        order_itself = Order.objects.get(id=order_id)
        orderchecking_itself = OrderChecking.objects.get(order=order_id)
        if not order_itself.renter:
            order_itself.renter = renter
            orderchecking_itself.confirmed = is_accept
            orderchecking_itself.renter = renter
            orderchecking_itself.save()
            order_itself.save()
            return Response({"details": "order accepted"}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "there is already accepted renter"}, status=status.HTTP_400_BAD_REQUEST)
