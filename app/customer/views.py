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


# Create your views here.

class CustomerProfileAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        user = request.user
        customer = CustomerProfile.objects.all()
        # user_serializer = UserSerializer(user, many=True)
        customer_serializer = CustomerSerializer(customer, many=True)
        # data = {"user": user_serializer.data, "user_profile": customer_serializer.data}
        return Response(customer_serializer.data)

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
    # permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'customer_address': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),
        }
    ))
    def post(self, request):
        data = request.data
        # try:
        user = User.objects.get(id=data["user_id"])
        customer = CustomerProfile.objects.create(
            phone_number=data["phone_number"],
            customer_address=data["customer_address"],
            user=user
        )
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    token = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        countries = Country.objects.all()
        countrySerializer = CountrySerializer(countries, many=True, context={"request": request})
        return Response(data=countrySerializer.data, status=status.HTTP_200_OK)


class RegionAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    token = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
