from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import ManagerProfile
from .serializers import ManagerSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from utilities.pagination import PaginationHandlerMixin
from equipments.views import BasicPagination


# Create your views here.
class RegisterManagerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagerSerializer
    parser_classes = (MultiPartParser, FormParser)
    token = openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING)
    password = openapi.Parameter(
        'password', in_=openapi.IN_FORM,
        description='enter password',
        type=openapi.TYPE_STRING
    )
    pre_password = openapi.Parameter(
        'pre_password', in_=openapi.IN_FORM,
        description='enter pre_password',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token, password, pre_password], parser_classes=parser_classes,
                         request_body=serializer_class)
    def post(self, request):
        data = request.data
        user_itself = request.user
        if data["password"] == data["pre_password"]:
            # manager = ManagerProfile.objects.create(
            #     user=user_itself,
            #     image=null,
            #     bio="bio",
            # )
            serializer = ManagerSerializer(data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "password not match"}, status=status.HTTP_400_BAD_REQUEST)


class ManagerAPIView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagerSerializer
    pagination_class = BasicPagination
    parser_classes = (MultiPartParser, FormParser)
    token = openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token])
    def get(self, request):
        managers = ManagerProfile.objects.all()
        page = self.paginate_queryset(managers)
        serializer = ManagerSerializer(page, many=True)
        if page is not None:
            serializer = self.get_paginated_response(
                ManagerSerializer(page, many=True).data)
        else:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data
            )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes, request_body=serializer_class)
    def put(self, request):
        user_itself = request.user
        manager = ManagerProfile.objects.get(user=user_itself)
        serializer = ManagerSerializer(manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user_itself = request.user
            manager = ManagerProfile.objects.get(user=user_itself)
            manager.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
