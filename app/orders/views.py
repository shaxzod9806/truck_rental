from django.shortcuts import render
from .models import Order, OrderChecking, FireBaseNotification
from index.models import User
from renter.serializers import UserSerializer
from customer.models import CustomerProfile
from .serializers import OrderSerializer, FireBaseNotificationSerializer
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
from utilities.sms import send_confirm_sms, send_accepted_sms
from utilities.firebase import send_notification
from utilities.price_calculation import renting_time_calc
from equipments.views import BasicPagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from utilities.pagination import PaginationHandlerMixin
from django.utils.dateparse import parse_datetime

from utilities.firebase import send_notification


# Create your views here.


class FireBaseView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        notifications = FireBaseNotification.objects.all()
        serializer = FireBaseNotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[param_config], request_body=FireBaseNotificationSerializer,
                         parser_classes=parser_classes)
    def post(self, request):
        serializer = FireBaseNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RefreshFireBaseTokenView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        usr = request.user
        fmc_token = User.objects.get(id=usr.id).fmc_token
        return Response(
            {'user': usr.username, 'first_name': usr.first_name, 'fmc_token': fmc_token}
        )

    fmc_token = openapi.Parameter(
        'fmc_token', in_=openapi.IN_QUERY,
        description='enter fmc_token',
        type=openapi.TYPE_STRING
    )
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY,
        description='enter user id',
        type=openapi.TYPE_INTEGER
    )
    acc_token = openapi.Parameter(
        'acc_token', in_=openapi.IN_QUERY,
        description='enter token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[acc_token, fmc_token, user_id])
    def put(self, request):
        user_id = request.GET.get('user_id')
        fmc_token_new = request.GET.get('fmc_token')
        fmc_token = User.objects.filter(id=user_id).update(fmc_token=fmc_token_new)
        usr = User.objects.get(id=user_id)
        tokens = get_tokens_for_user(usr)
        # token = AccessToken.for_user(user=usr)
        # print(tokens)
        # user_refresh_token = User.objects.get(id=usr.id)
        # token = AccessToken.for_user(usr)
        return Response({'user': usr.username, 'first_name': usr.first_name,
                         'fmc_token': fmc_token_new, 'token': tokens})


class OrderAPIView(APIView, PaginationHandlerMixin):
    # Test here for changing
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
            # Notify the user about the order
            renter = renter_profile.objects.get(id=near_equipment["renter_id"])
            #  This should be function outside of view
            start_time = data["start_time"]
            end_time = data["end_time"]
            order_price = data["order_price"]
            address = data["address"]
            data["order_price"] = data["order_price"]
            data["payment_type"] = data["payment_type"]
            data["notes"] = data["notes"]
            data["quantity"] = data["quantity"]
            data["night_hours"] = data["night_hours"]
            data["daylight_hours"] = data["daylight_hours"]
            # data["renter"] = renter.id
            print(data)
            data["renter"] = None
            orderjon = Order.objects.get(id=data["id"])
            orderjon.start_time = parse_datetime(start_time)
            orderjon.end_time = parse_datetime(end_time)
            send_confirm_sms(renter, SMS, start_time, end_time, order_price, address)
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
    lang = openapi.Parameter('lang', in_=openapi.IN_QUERY, description='uz, en, ru', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config, ordering, lang])
    def get(self, request):

        lang = request.GET.get('lang')
        print(lang)
        orders = Order.objects.filter(customer=request.user).order_by('-id')
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
    lang = openapi.Parameter('lang', in_=openapi.IN_QUERY, description='uz, en, ru', type=openapi.TYPE_STRING)
    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )

    @swagger_auto_schema(manual_parameters=[token, lang], parser_classes=parser_classes)
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
            # notif = send_notification("order cancel", "motochas v2 chiqdi",
            #                           "e9_-MzJ3Se2VUhVnCFoLo3:APA91bHFIjL0zw0qqHvbmeFaYpfJMFXMnjpQBErPGSIlPIN8_pNpn4siVbP3fyA_lJYo_ohU1XtKiD8aBethRh_sqWkwTadzFWHQnKMaRk0wUq3iztyCfwyLM_RaZeW2q5qFnTdlKblK",
            #                           "image_url")
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
        is_accept = int(request.GET.get('is_accept'))
        renter = request.user
        order_itself = Order.objects.get(id=order_id)
        orderchecking_itself = OrderChecking.objects.get(order=order_id)
        if not order_itself.renter:
            order_itself.renter = renter
            orderchecking_itself.confirmed = is_accept
            orderchecking_itself.renter = renter
            orderchecking_itself.save()
            order_itself.save()
            if is_accept == 3:
                send_accepted_sms(order_itself.customer, SMS, order_itself.start_time, order_itself.end_time,
                                  order_itself.order_price, order_itself.address)
                title = "Order accepted"
                body = "Renter orderingizni qabul qildi"
                usr = order_itself.customer
                print("==========================================================")

                print(usr)
                image_url = "image.jpg"
                # image_url = "https://www.briarwoodanimalhospital.com/wp-content/uploads/sites/28/2016/08/hairballcats.jpg"

                fcm_token = usr.fmc_token
                print("==========================================================")
                print(fcm_token)
                notif = send_notification(title=title, body=body, image_url=image_url, fcm_token=fcm_token)
                fb_notif = FireBaseNotification.objects.create(
                    title=title,
                    body=body,
                    user=usr,
                    type_notification=1,
                    oreder_id=order_itself.id,
                    image_url=image_url,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                serializer = FireBaseNotificationSerializer(fb_notif, many=False)
                print(fb_notif.oreder_id)
                return Response({"details": "order accepted"}, status=status.HTTP_200_OK)
            elif is_accept == 2:
                # send_canceled_sms(order_itself.customer, SMS, order_itself.start_time, order_itself.end_time,
                #                   order_itself.order_price, order_itself.address)
                title = "Order canceled"
                body = "Renter orderingizni qabul qilmadi"
                usr = order_itself.customer
                print("==========================================================")

                print(usr)
                # image_url = "image.jpg"
                image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxJZpcoAj-KAJNZV_PSQ_Rqz-9gTnfvF1uJw&usqp=CAU"
                fcm_token = usr.fmc_token
                print("==========================================================")
                print(fcm_token)
                notif = send_notification(title=title, body=body, image_url=image_url, fcm_token=fcm_token)
                fb_notif = FireBaseNotification.objects.create(
                    title=title,
                    body=body,
                    user=usr,
                    type_notification=2,
                    oreder_id=order_itself.id,
                    image_url=image_url,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                serializer = FireBaseNotificationSerializer(fb_notif, many=False)
                print(fb_notif.oreder_id)
            return Response({"details": "order canceled"}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "there is already accepted renter"}, status=status.HTTP_400_BAD_REQUEST)
