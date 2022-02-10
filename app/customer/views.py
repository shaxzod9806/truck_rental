from renter.serializers import User
from .serializers import CustomerSerializer, CountrySerializer, RegionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import CustomerProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from index.models import User
from .models import Country, Region
from renter.serializers import UserSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from utilities.pagination import PaginationHandlerMixin
from equipments.views import BasicPagination


# Create your views here.

class CustomerProfileAPI(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = BasicPagination

    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        customers = CustomerProfile.objects.all()
        # print(customers)
        page = self.paginate_queryset(customers)
        serializer = CustomerSerializer(page, many=True)
        # print(serializer.data)
        if page is not None:
            serializer = self.get_paginated_response(
                CustomerSerializer(page, many=True).data)
        else:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data
            )
        # print(f"serializer.data   {serializer.data}")
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    profile_id = openapi.Parameter(
        'profile_id', in_=openapi.IN_FORM,
        description='enter user profile id',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[param_config, profile_id], request_body=CustomerSerializer)
    def put(self, request):
        customer_profile = CustomerProfile.objects.get(id=request.data["profile_id"])
        customer_profile_serializer = CustomerSerializer(customer_profile, many=False, data=request.data)
        if customer_profile_serializer.is_valid():
            customer_profile_serializer.save()
            return Response(customer_profile_serializer.data, status=status.HTTP_200_OK)
        return Response(customer_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[param_config, profile_id], request_body=CustomerSerializer)
    def delete(self, request):
        try:
            customer_profile = CustomerProfile.objects.get(id=request.data['profile_id'])
            customer_profile.delete()
            return Response('customer is deleted', status=status.HTTP_200_OK)
        except:
            return Response('customer is not found', status=status.HTTP_400_BAD_REQUEST)


class CustomerRegisterAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    parser_classes=[MultiPartParser,FormParser]
    http_method_names = ['post']

    token = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )
    @swagger_auto_schema(manual_parameters=[token],request_body=CustomerSerializer,)
    def post(self,request):
        data=request.data
        user=User.objects.get(id=request.data["user"])
        country=Country.objects.get(id=request.data["country"])
        region=Region.objects.get(id=request.data["region"])
        customer=CustomerProfile.objects.create(
            phone_number=data["phone_number"],
            country=country,
            region=region,
            customer_address=data["customer_address"],
            user=user
        )
        serializer=CustomerSerializer(customer,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    # @swagger_auto_schema(request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     properties={
    #         'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
    #         'customer_address': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
    #         'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),
    #         'country': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),
    #         'region': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),
    #         'token': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
    #     }
    # ))
    # def post(self, request):
    #     data = request.data
    #     # try:
    #     user = User.objects.get(id=data["user_id"])
    #     country = Country.objects.get(id=data["country"])
    #     region = Region.objects.get(id=data["region"])
    #     customer = CustomerProfile.objects.create(
    #         phone_number=data["phone_number"],
    #         customer_address=data["customer_address"],
    #         country=country,
    #         region=region,
    #         user=user
    #     )
    #     serializer = CustomerSerializer(customer, many=False)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class CountryAPI(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    # token = openapi.Parameter(
    #     'Authorization', in_=openapi.IN_HEADER,
    #     description='enter access token with Bearer word for example: Bearer token',
    #     type=openapi.TYPE_STRING)

    # @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        countries = Country.objects.all()
        countrySerializer = CountrySerializer(countries, many=True, context={"request": request})
        return Response(data=countrySerializer.data, status=status.HTTP_200_OK)


class RegionAPI(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    # token = openapi.Parameter(
    #     'Authorization', in_=openapi.IN_HEADER,
    #     description='enter access token with Bearer word for example: Bearer token',
    #     type=openapi.TYPE_STRING
    # )

    # country = openapi.Parameter(
    #     'country', in_=openapi.IN_FORM,
    #     description='enter country id',
    #     type=openapi.TYPE_INTEGER
    # )

    country_id = openapi.Parameter(
        'country_id', in_=openapi.IN_QUERY,
        description='country_id',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[country_id])
    def get(self, request):
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(request.GET.get("country_id"))
        regions = Region.objects.filter(country=request.GET.get("country_id"))
        serializer = RegionSerializer(regions, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
