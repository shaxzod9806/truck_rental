from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from index.models import User
from django.contrib.auth.hashers import make_password
from renter.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
import random
from utilities.models import SMS
from utilities.sms import send_sms


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["user_type"] = self.user.user_type
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["user_id"] = self.user.id
        # data["password"] = self.user.password

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
        random_number = random.randrange(10000, 99999)
        # try:
        user = User.objects.create(
            first_name=data["first_name"],
            username=data["username"],
            password=make_password(data["password"]),
            user_type=data["user_type"],
            is_active=False,
            activation_code=random_number
        )
        serializer = UserSerializer(user, many=False)
        sms_itself = SMS.objects.create(phone_number=user.username, text=random_number)
        if not user.is_active:
            send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
        sms_itself.is_sent = 1
        return Response(serializer.data)
        # except:
        #     message = {'detail': "User with this username already exist"}
        #     return Response(message, status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    user_id = openapi.Parameter(
        'user_id',
        in_=openapi.IN_QUERY,
        description='Enter user id to verify the user ',
        type=openapi.TYPE_INTEGER
    )
    verification_code = openapi.Parameter(
        'verification_code',
        in_=openapi.IN_QUERY,
        description='Enter verification_code to verify the user ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[user_id, verification_code])
    def post(self, request):
        user_id = request.GET.get("user_id")
        verification_code = request.GET.get("verification_code")
        user_itself = User.objects.get(id=user_id)
        print('if out')
        if user_itself.is_active:
            print('User is already activated')
            return Response("User is already activated")
        if int(verification_code) == int(user_itself.activation_code):
            user_itself.is_active = True
            user_itself.save()
            return Response("User is successfully activated", status=status.HTTP_200_OK)
        else:
            return Response("Activation code is wrong", status=status.HTTP_400_BAD_REQUEST)


class ResetPhoneNumber(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
        }
    ))
    def post(self, request):
        random_number = random.randrange(10000, 99999)
        phone_number = request.data['phone_number']
        print(phone_number)
        user = User.objects.get(username=phone_number)
        sms_itself = SMS.objects.create(
            phone_number=user.username, text=random_number
        )
        if user.is_active:
            send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
            sms_itself.is_sent = 1
            sms_itself.sms_type = 2
            user.activation_code = random_number
            user.save()
            print(user.activation_code)
            user_serializer = UserSerializer(user, many=False)
            print(user.id)
            return Response(
                f"sms is send to  id: {user.id}    PN:{sms_itself.phone_number}     type:{user.user_type}      successfully"
            )

        return Response('something is wrong')


class ResetVerifyUserCode(APIView):
    user_id = openapi.Parameter(
        'user_id',
        in_=openapi.IN_QUERY,
        description='Enter user id to verify the user ',
        type=openapi.TYPE_INTEGER
    )
    verification_code = openapi.Parameter(
        'verification_code',
        in_=openapi.IN_QUERY,
        description='Enter verification_code to verify the user ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[user_id, verification_code])
    def post(self, request):
        user_id = request.GET.get('user_id')
        verification_code = request.GET.get('verification_code')

        user_itself = User.objects.get(id=user_id)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(user_itself)
        if not user_itself.is_active:
            print("user in not activ")
            return Response("User is not actived,you must first register")
        print('=====================================================')
        print(verification_code)
        print(user_itself.activation_code)
        # user_itself.activation_code =
        if int(verification_code) == int(user_itself.activation_code):
            user_itself.save()
            return Response('verification code is correct', status=status.HTTP_200_OK)
        else:
            return Response("verification is not correct ", status=status.HTTP_400_BAD_REQUEST)


class Reset_New_Password(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'pre_password': openapi.Schema(type=openapi.TYPE_STRING, description='pre_password'),
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
        }
    ))
    def post(self, request):
        password = request.data['password']
        pre_password = request.data['pre_password']
        print(password)
        user_id = request.data['user_id']
        user = User.objects.get(id=user_id)
        if pre_password == password:
            user.password = make_password(password)
            user.last_name = password  # FOR CHEKKING
            user.save()
            print(user.password)
            return Response('new password is created', status=status.HTTP_200_OK)
        return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
