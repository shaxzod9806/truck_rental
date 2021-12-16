from django.shortcuts import render
# Create your views here.

from .serializers import UserSerializer, ProfileSerializer, FilesSerializer
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
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser


class UserProfile(APIView):
    permission_classes = [IsAuthenticated, IsRenter]
    parser_classes = (MultiPartParser, FormParser)

    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config], )
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user.id)
        user_serializer = UserSerializer(user, many=False)
        profile_serializer = ProfileSerializer(profile, many=False)
        data = {"user": user_serializer.data, "user_profile": profile_serializer.data}
        return Response(data)

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
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'organization': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'office_address': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),

        }
    ))
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(id=data["user_id"])
            profile = Profile.objects.create(
                phone_number=data["phone_number"],
                organization=data["organization"],
                office_address=data["office_address"],
                user=user
            )
            serializer = ProfileSerializer(profile, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            message = {'detail': "Something went Wrong"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class FileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRenter]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FilesSerializer
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    files_id = openapi.Parameter(
        'files_id', in_=openapi.IN_FORM,
        description='enter files ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(request_body=FilesSerializer, parser_classes=parser_classes,
                         manual_parameters=[files_id, param_config])
    def put(self, request):
        user = request.user
        files = Files.objects.get(user=user.id)
        files_serializer = FilesSerializer(files, many=True, data=request.data)
        if files_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parammetrs=[param_config], parser_classes=parser_classes)
    def get(self, request):
        # user = request.user
        files = Files.objects.all()
        user_serializer = UserSerializer(user, many=True)
        files_serializer = FilesSerializer(files, many=True)
        data = {"user": user_serializer.data, "user_files": files_serializer.data}
        return Response(data)

    @swagger_auto_schema(manual_parameters=[param_config], request_body=FilesSerializer)
    def post(self, request):
        serializer = FilesSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

    files_id = openapi.Parameter(
        'files_id', in_=openapi.IN_FORM,
        description='enter files ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[files_id, param_config])
    def delete(self, request):
        try:
            files = Equipment.objects.get(id=int(request.data["files_id"]))
            files.delete()
            return Response({"detail": "files is deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "files does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class SingleFileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )
    files_id = openapi.Parameter(
        'files_id', in_=openapi.IN_BODY,
        description='enter files_id',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parametrs=[param_config])
    def get(self, request, pk):
        try:
            files = Files.objects.get(id=pk)
            serializer = FilesSerializer(files, many=False)
            return Response(serializer.data)
        except:
            return Response({'detail': 'File does not exist'})
