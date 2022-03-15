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
import random
from utilities.models import SMS
from utilities.sms import send_sms
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["user_type"] = self.user.user_type
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["user_id"] = self.user.id
        data["is_active"] = self.user.is_active
        data["device_id"] = self.user.device_id

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Device_idView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    user_id = openapi.Parameter('user_id', openapi.IN_FORM, description="user_id", type=openapi.TYPE_INTEGER)
    device_id = openapi.Parameter('device_id', openapi.IN_FORM, description="device_id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[user_id, device_id])
    def post(self, request):
        user_itself = User.objects.get(id=request.data['user_id'])
        device_id = request.data.get('device_id')
        user_device_id = user_itself.device_id
        if user_device_id == device_id:
            return Response({"message": "Device id is correct"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SecondRegistration_userID_API(APIView):
    serializer_class = UserSerializer
    http_method_names = ["post"]
    user_id = openapi.Parameter(
        'user_id',
        in_=openapi.IN_QUERY,
        description='enter user_id ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[user_id])
    def post(self, request):
        random_number = random.randrange(10000, 99999)
        user_id = request.GET.get("user_id")
        user_itself = User.objects.get(id=user_id)
        user_itself.activation_code = random_number
        serializer = UserSerializer(user_itself, many=False)
        user_itself.save()
        if user_itself.is_active:
            return Response({"details": "user already active", "is_active": user_itself.is_active},
                            status=status.HTTP_400_BAD_REQUEST)
        sms_itself = SMS.objects.create(
            phone_number=user_itself.username,
            text=f"""Xayrli kun  {(user_itself.first_name).capitalize()} 
            Bu sizning tasdiqlash kodingiz: {random_number},
                """
        )
        send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
        sms_itself.is_sent = 1
        return Response(serializer.data, status=status.HTTP_200_OK)


class SecondRegistrationAPI(APIView):
    serializer_class = UserSerializer
    http_method_names = ["post"]
    verification_code = openapi.Parameter(
        'verification_code',
        in_=openapi.IN_QUERY,
        description='enter verification_code ',
        type=openapi.TYPE_INTEGER
    )
    user_id = openapi.Parameter(
        'user_id',
        in_=openapi.IN_QUERY,
        description='enter user_id ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[verification_code, user_id])
    def post(self, request):
        user_id = request.GET.get("user_id")
        user_itself = User.objects.get(id=user_id)
        serializer = UserSerializer(user_itself, many=False)
        verification_code = request.GET.get("verification_code")

        if int(user_itself.activation_code) == int(verification_code):
            user_itself.is_active = True
            user_itself.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(CreateAPIView):
    serializer_class = UserSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'user_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),
            'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
        }
    ))
    def post(self, request):
        data = request.data
        random_number = random.randrange(10000, 99999)
        if len(data['password']) < 8:
            return Response({"message": "password must be more than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=make_password(data["password"]),
            user_type=data["user_type"],
            is_active=False,
            activation_code=random_number,
            device_id=data["device_id"]
        )
        serializer = UserSerializer(user, many=False)
        sms_itself = SMS.objects.create(phone_number=user.username,
                                        text=data["first_name"] + " bu sizning Tasdiqlash kodingiz: " + str(
                                            random_number))
        if not user.is_active:
            send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
        sms_itself.is_sent = 1
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if user_itself.is_active:
            return Response(
                "User is already activated",
                status=status.HTTP_400_BAD_REQUEST
            )
        if int(verification_code) == int(user_itself.activation_code):
            user_itself.is_active = True
            user_itself.save()
            return Response({"details": "User is successfully activated",
                             "is_active": {user_itself.is_active}},
                            status=status.HTTP_200_OK)
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
            user_serializer = UserSerializer(user, many=False)
            user_info = {"user_id": user.id, "is_active": user.is_active, "phone_number": sms_itself.phone_number,
                         "user_type": user.user_type}
            return Response(user_info, status=status.HTTP_200_OK)
        return Response('something is wrong', status=status.HTTP_400_BAD_REQUEST)


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
        if not user_itself.is_active:
            return Response("User is not actived,you must first register", status=status.HTTP_400_BAD_REQUEST)
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
        user_id = request.data['user_id']
        user = User.objects.get(id=user_id)
        if pre_password == password:
            user.password = make_password(password)
            user.save()
            return Response({"detail": 'new password is created', "is_active": user.is_active},
                            status=status.HTTP_200_OK)
        return Response({"detail": 'something went wrong', "is_active": user.is_active},
                        status=status.HTTP_400_BAD_REQUEST)


class UserEditAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializers = UserSerializer
    token = openapi.Parameter(
        "Authorization", in_=openapi.IN_HEADER,
        description="enter access token with Bearer word for example: Bearer token",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(request_body=UserSerializer, manual_parameters=[token])
    def put(self, request):
        user = request.user
        data = request.data
        user_itself = User.objects.get(id=user.id)
        user_serializer = UserSerializer(user_itself, many=False, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Change_new_password(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializers = UserSerializer
    token = openapi.Parameter(
        "Authorization", in_=openapi.IN_HEADER,
        description="enter access token with Bearer word for example: Bearer token",
        type=openapi.TYPE_STRING
    )
    old_password = openapi.Parameter('old_password', openapi.IN_FORM, description="old_password",
                                     type=openapi.TYPE_STRING)
    new_password = openapi.Parameter('new_password', openapi.IN_FORM, description="new_password",
                                     type=openapi.TYPE_STRING)
    pre_password = openapi.Parameter('pre_password', openapi.IN_FORM, description="pre_password",
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token, old_password, new_password, pre_password])
    def post(self, request):
        user = request.user
        user_itself = User.objects.get(id=user.id)
        if user_itself.check_password(request.data['old_password']):
            if request.data['pre_password'] == request.data['new_password']:
                user_itself.set_password(request.data['new_password'])
                user_itself.save()
                return Response({"detail": 'new password is created'},
                                status=status.HTTP_200_OK)
            else:
                return Response({"detail": 'new password is not correct'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": 'old password is not correct'},
                            status=status.HTTP_400_BAD_REQUEST)


class SingleUserAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializers = UserSerializer
    token = openapi.Parameter(
        "Authorization", in_=openapi.IN_HEADER,
        description="enter access token with Bearer word for example: Bearer token",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        user_id = request.user.id
        user_itself = User.objects.get(id=user_id)
        user_serializer = UserSerializer(user_itself, many=False)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
