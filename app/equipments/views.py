from rest_framework.response import Response
from rest_framework import status

from .serializers import CategorySerializer, SubCatSerializer, EquipmentsSerializer, AdditionsSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from .models import Category, SubCategory, Equipment, AdditionalProps
# Create your views here.

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Offset pegination is added to category need to test
class CategoryAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(request_body=CategorySerializer, parser_classes=parser_classes, manual_parameters=[param_config])
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cat_id = openapi.Parameter('cat_id', in_=openapi.IN_FORM,
                               description='enter category ID',
                               type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(request_body=CategorySerializer, parser_classes=parser_classes,
                         manual_parameters=[cat_id, param_config])
    def put(self, request):
        cat_id = request.data["cat_id"]
        category = Category.objects.get(id=int(cat_id))
        serializer = CategorySerializer(category, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[cat_id, param_config])
    def delete(self, request):
        try:
            category = Category.objects.get(id=int(request.data["cat_id"]))
            category.delete()
            return Response({"detail": "category is deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Category does not exist"})

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)
    cat_id = openapi.Parameter('cat_id', in_=openapi.IN_BODY,
                               description='enter cat_id',
                               type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data)
        except:
            return Response({"detail": "category does not exist"})


class SubCatApi(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(request_body=SubCatSerializer, parser_classes=parser_classes, manual_parameters=[param_config])
    def post(self, request):
        serializer = SubCatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    sub_cat_id = openapi.Parameter('sub_cat_id', in_=openapi.IN_FORM,
                                   description='enter Subcategory ID',
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(request_body=SubCatSerializer, parser_classes=parser_classes,
                         manual_parameters=[sub_cat_id, param_config])
    def put(self, request):
        cat_id = request.data["sub_cat_id"]
        sub_category = SubCategory.objects.get(id=int(cat_id))
        serializer = SubCatSerializer(sub_category, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[sub_cat_id, param_config])
    def delete(self, request):
        try:
            sub_cat = SubCategory.objects.get(id=int(request.data["sub_cat_id"]))
            sub_cat.delete()
            return Response({"detail": "category is deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Category does not exist"})

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        category = SubCategory.objects.all()
        serializer = SubCatSerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleSubCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)
    cat_id = openapi.Parameter('sub_cat_id', in_=openapi.IN_BODY,
                               description='enter sub_cat_id',
                               type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            sub_category = SubCategory.objects.get(id=pk)
            serializer = SubCatSerializer(sub_category, many=False)
            return Response(serializer.data)
        except:
            return Response({"detail": "category does not exist"})


class EquipmentAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config], request_body=EquipmentsSerializer,
                         parser_classes=parser_classes)
    def post(self, request):
        serializer = EquipmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    equipment_id = openapi.Parameter('equipment_id', in_=openapi.IN_FORM,
                                     description='enter equipment ID',
                                     type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(request_body=EquipmentsSerializer, parser_classes=parser_classes,
                         manual_parameters=[equipment_id, param_config])
    def put(self, request):
        cat_id = request.data["equipment_id"]
        equipment = Equipment.objects.get(id=int(cat_id))
        serializer = EquipmentsSerializer(equipment, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[equipment_id, param_config])
    def delete(self, request):
        try:
            equipment = Equipment.objects.get(id=int(request.data["equipment_id"]))
            equipment.delete()
            return Response({"detail": "equipment is deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "equipment does not exist"})

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = SubCatSerializer(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleEquipment(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            equipment = Equipment.objects.get(id=pk)
            serializer = SubCatSerializer(equipment, many=False)
            return Response(serializer.data)
        except:
            return Response({"detail": "Equipment does not exist"})


class AdditionsApi(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config], request_body=AdditionsSerializer)
    def post(self, request,  parser_classes=parser_classes):
        serializer = AdditionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    addition_id = openapi.Parameter('addition_id', in_=openapi.IN_FORM, description='enter addition_id ',
                                    type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[addition_id, param_config], request_body=AdditionsSerializer,
                         parser_classes=parser_classes)
    def put(self, request):
        addition_id = request.data["addition_id"]
        addition = AdditionalProps.objects.get(id=int(addition_id))
        serializer = AdditionsSerializer(addition, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        addition = AdditionalProps.objects.all()
        serializer = AdditionsSerializer(addition, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[addition_id, param_config])
    def delete(self, request):
        try:
            addition = AdditionalProps.objects.get(id=int(request.data["addition_id"]))
            addition.delete()
            return Response({"detail": "addition is deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "addition does not exist"})


class SingleAddition(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            addition = AdditionalProps.objects.get(id=pk)
            serializer = AdditionsSerializer(addition, many=False)
            return Response(serializer.data)
        except:
            return Response({"detail": "Addition does not exist"})



















