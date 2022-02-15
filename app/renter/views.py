from django.shortcuts import render
from .models import RenterProduct
# Create your views here.

from .serializers import UserSerializer, ProfileSerializer, FilesSerializer, RenterProductSerializer
from orders.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Profile, Files
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from index.permissions import IsRenter
from rest_framework.generics import CreateAPIView
from index.models import User
from customer.models import Country, Region
from orders.models import Order, OrderChecking
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from utilities.mapping import find_near_equipment
from utilities.models import SMS
from utilities.sms import send_sms
from utilities.pagination import PaginationHandlerMixin
from equipments.views import BasicPagination


class RenterOrdersAPI(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = BasicPagination
    serializer_class = OrderSerializer
    token = openapi.Parameter(
        "Authorization", in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )
    ordering = openapi.Parameter(
        'ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description='Enter field name to order for example: "order_name" ascending; '
                    'put "-" for reverse ordering: "-order_name"'
    )

    @swagger_auto_schema(manual_parameters=[token, ordering])
    def get(self, request):
        user_itself = request.user
        # user_itself = User.objects.get(id=id_user)
        if user_itself.user_type == 3:
            order_checking_obj = OrderChecking.objects.filter(renter=user_itself)
            # print(order_checking_obj.values())
            render_orders = []
            for i in range(order_checking_obj.count()):
                render_orders += Order.objects.filter(id=order_checking_obj[i].order.id)
            page = self.paginate_queryset(render_orders)
            if page is not None:
                serializer = self.get_paginated_response(
                    OrderSerializer(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True, context={"request": request}).data)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[param_config], )
    def get(self, request):
        # print('=============================================================')
        user = request.user
        # print(user)
        profile = Profile.objects.all()
        # profile = Profile.objects.get(user=user.id)
        user_serializer = UserSerializer(user, many=True)
        profile_serializer = ProfileSerializer(profile, many=True)
        return Response(profile_serializer.data)

    @swagger_auto_schema(request_body=ProfileSerializer, manual_parameters=[param_config])
    def put(self, request):
        user = request.user
        print(request.data)
        profile = Profile.objects.get(user=user.id)
        profile_serializer = ProfileSerializer(profile, many=False, data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[param_config])
    def delete(self, request):
        try:
            user = request.user
            profile = Profile.objects.get(user=user.id)
            profile.delete()
            return Response("profile deleted", status=status.HTTP_200_OK)
        except:
            return Response("profile not found", status=status.HTTP_400_BAD_REQUEST)


class ProfileRegister(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    # http_method_names = ['post']

    token = openapi.Parameter(
        "Authorization", in_=openapi.IN_HEADER,
        description="enter access token with Bearer word for example: Bearer token",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes,
                         request_body=ProfileSerializer)
    def post(self, request):
        data = request.data
        # try:
        user = User.objects.get(id=data["user"])
        # user.user_type = 3
        print(user.user_type)
        profile = Profile.objects.create(
            organization=data["organization"],
            office_address=data["office_address"],
            country=Country.objects.get(id=data["country"]),
            region=Region.objects.get(id=data["region"]),
            user=user,
        )
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # except:
    #     message = {'detail': "Something went Wrong"}


#     return Response(message, status=status.HTTP_400_BAD_REQUEST)


# =============================RenterProduct=================================================================


class RentrProductAPI(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = RenterProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        user_id = request.user.id
        renter_id = Profile.objects.get(user=user_id)
        renter_products = RenterProduct.objects.filter(renter=renter_id)
        # print(renter_products)
        page = self.paginate_queryset(renter_products)
        serializer = RenterProductSerializer(page, many=True)
        # print(serializer.data)
        if page is not None:
            serializer = self.get_paginated_response(
                RenterProductSerializer(page, many=True).data)
        else:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True)
            )
        print(serializer.data)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[param_config], parser_classes=parser_classes,
                         request_body=RenterProductSerializer)
    def post(self, request):
        rentr_p_seriializer = RenterProductSerializer(data=request.data, many=False)
        if rentr_p_seriializer.is_valid():
            rentr_p_seriializer.save()
            return Response(rentr_p_seriializer.data, status=status.HTTP_200_OK)
        return Response(rentr_p_seriializer.errors, status=status.HTTP_400_BAD_REQUEST)

    renter_product_id = openapi.Parameter(
        'renter_product_id', in_=openapi.IN_FORM,
        description='enter renter_product ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[param_config, renter_product_id], request_body=RenterProductSerializer)
    def put(self, request):
        renter_p_id = request.data["renter_product_id"]
        renter_p = RenterProduct.objects.get(id=renter_p_id)
        serializer = RenterProductSerializer(renter_p, many=False, data=request.data)
        user_type = renter_p.renter.user.user_type
        if serializer.is_valid() and user_type <= 3:
            serializer.save()
            return Response({"details": "renter product updated"}, serializer.data, status=status.HTTP_200_OK)
        return Response({"details": "renter product not updated"}, serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[renter_product_id, param_config])
    def delete(self, request):
        try:
            renter_product_id = request.data["renter_product_id"]
            renter_product = RenterProduct.objects.get(id=int(renter_product_id))
            renter_product.delete()
            return Response({"detail": "renter product deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "renter product not found"}, status=status.HTTP_400_BAD_REQUEST)


class SingleRentrProductAPI(APIView):
    permission_classes = [IsAuthenticated]
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            renter_product = RenterProduct.objects.get(id=pk)
            serializer = RenterProductSerializer(renter_product, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Renter product is not found"}, status=status.HTTP_400_BAD_REQUEST)
