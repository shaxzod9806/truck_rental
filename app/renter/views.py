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
from orders.models import Order
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
        if user_itself.user_type == 3:
            render_orders = Order.objects.filter(renter=user_itself)
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
        # print(profile)
        # profile = Profile.objects.get(user=user.id)
        user_serializer = UserSerializer(user, many=True)
        # print(user)
        profile_serializer = ProfileSerializer(profile, many=True)
        # print(profile_serializer)
        # data = {"user": user_serializer.data, "user_profile": profile_serializer.data}
        # print(profile_serializer.data)
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


class ProfileRegister(CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # 'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'organization': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'office_address': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),

        }
    ))
    def post(self, request):
        data = request.data
        # try:
        user = User.objects.get(id=data["user_id"])
        profile = Profile.objects.create(
            # phone_number=data["phone_number"],
            organization=data["organization"],
            office_address=data["office_address"],
            user=user
        )
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # except:
    #     message = {'detail': "Something went Wrong"}


#     return Response(message, status=status.HTTP_400_BAD_REQUEST)


# =============================RenterProduct=================================================================


class RentrProductAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RenterProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[param_config], )
    def get(self, request):
        try:
            rentr_p = RenterProduct.objects.all()
            rentr_p_seriializer = RenterProductSerializer(rentr_p, many=True)
            return Response(rentr_p_seriializer.data, status=status.HTTP_200_OK)
        except:
            return Response(rentr_p_seriializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
