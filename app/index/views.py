from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from index.models import User
from django.contrib.auth.hashers import make_password
from renter.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["user_type"] = self.user.user_type
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["user_id"] = self.user.id

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegister(CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'user_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),

        }
        ))
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                first_name=data["first_name"],
                username=data["username"],
                password=make_password(data["password"]),
                user_type=data["user_type"]


            )
            serializer = UserSerializer(user, many=False)

            return Response(serializer.data)
        except:
            message = {'detail': "User with this username already exist"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


