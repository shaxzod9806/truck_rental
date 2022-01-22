from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, SubCatSerializer, EquipmentsSerializer, AdditionsSerializer, \
    CategorySerializerUz, SubCatSerializerUz, CategorySerializerRu, SubCatSerializerRu, CategorySerializerEn, \
    SubCatSerializerEn, EquipmentsSerializerUz, EquipmentsSerializerRu, EquipmentsSerializerEn, \
    BrandSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from .models import Category, SubCategory, Equipment, AdditionalProps, \
    Brand
# Create your views here.

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from utilities.pagination import PaginationHandlerMixin
from rest_framework import filters

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .pagination import LargeResultsSetPagination


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class BrandAPI(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    permission_class = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = BrandSerializer

    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(request_body=BrandSerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def post(self, request):
        serializer = BrandSerializer(data=request.data, many=False, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    brand_id = openapi.Parameter(
        'brand_id', in_=openapi.IN_FORM,
        description='enter brand ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(request_body=BrandSerializer, parser_classes=parser_classes,
                         manual_parameters=[brand_id, param_config])
    def put(self, request):
        brand_id = request.data["brand_id"]
        brand = Brand.objects.get(id=int(brand_id))
        serializer = BrandSerializer(brand, many=False, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[brand_id, param_config])
    def delete(self, request):
        try:
            brand = Brand.objects.get(id=int(request.data['brand_id']))
            brand.delete()
            return Response({'detail': 'Brand is deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Brand does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    ordering = openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                 description='Enter field name to order for example: "brand_name" ascending; '
                                             'put "-" for reverse ordering: "-brand_name"')

    @swagger_auto_schema(manual_parameters=[param_config, ordering])
    def get(self, request):
        brand = Brand.objects.all()
        page = self.paginate_queryset(brand)

        serializer = BrandSerializer(page, many=True, context={"request": request})
        if page is not None:
            serializer = self.get_paginated_response(BrandSerializer(page, many=True).data)
        else:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleBrandAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BrandSerializer
    parser_classes = (MultiPartParser, FormParser)

    token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                              description='enter access token', type=openapi.TYPE_STRING, )

    @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes)
    def get(self, request, pk):
        try:
            brand = Brand.objects.get(id=pk)
            serializer = BrandSerializer(brand, many=False, context={"request": request})
            return Response(serializer.data)
        except:
            return Response({'detail': 'Brand does not exist'})


class CategoryAPI(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = CategorySerializer
    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(request_body=CategorySerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def post(self, request):

        # serializer = CategorySerializer(data=request.data)
        serializer = CategorySerializer(data=request.data, many=False, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cat_id = openapi.Parameter(
        'cat_id', in_=openapi.IN_FORM,
        description='enter category ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(request_body=CategorySerializer, parser_classes=parser_classes,
                         manual_parameters=[cat_id, param_config])
    def put(self, request):
        cat_id = request.data["cat_id"]
        category = Category.objects.get(id=int(cat_id))
        serializer = CategorySerializer(category, many=False, data=request.data, context={"request": request})
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
            return Response({"detail": "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    # filter = openapi.Parameter('filter', in_=openapi.IN_QUERY, description='enter filter fields',
    #                            type=openapi.TYPE_STRING)
    lang = openapi.Parameter('lang', in_=openapi.IN_QUERY, description='uz, en, ru ', type=openapi.TYPE_STRING)
    ordering = openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                 description='Enter field name to order for example: "cat_name" ascending; '
                                             'put "-" for reverse ordering: "-cat_name"')

    @swagger_auto_schema(manual_parameters=[param_config, lang, ordering])
    def get(self, request):
        category = Category.objects.all()
        page = self.paginate_queryset(category)
        lang = request.GET.get("lang")

        serializer = CategorySerializer(page, many=True, context={"request": request})
        if page is not None:
            if lang == "uz":
                serializer = self.get_paginated_response(
                    CategorySerializerUz(page, many=True, context={"request": request}).data)
            elif lang == "ru":
                serializer = self.get_paginated_response(
                    CategorySerializerRu(page, many=True, context={"request": request}).data)
            elif lang == "en":
                serializer = self.get_paginated_response(
                    CategorySerializerEn(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True, context={"request": request}).data)
        else:
            if lang == "uz":
                serializer = self.get_paginated_response(
                    CategorySerializerUz(page, many=True, context={"request": request}).data)
            elif lang == "ru":
                serializer = self.get_paginated_response(
                    CategorySerializerRu(page, many=True, context={"request": request}).data)
            elif lang == "en":
                serializer = self.get_paginated_response(
                    CategorySerializerEn(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True, context={"request": request}).data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)
    cat_id = openapi.Parameter('cat_id', in_=openapi.IN_BODY,
                               description='enter cat_id',
                               type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category, many=False, context={"request": request})
            return Response(serializer.data)
        except:
            return Response({"detail": "category does not exist"})


class SubCatApi(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SubCatSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name_uz', 'name_ru', 'name_en']

    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(request_body=SubCatSerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def post(self, request):
        serializer = SubCatSerializer(data=request.data, many=False, context={"request": request})
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
        sub_cat_id = request.data["sub_cat_id"]
        sub_category = SubCategory.objects.get(id=int(sub_cat_id))
        serializer = SubCatSerializer(sub_category, data=request.data, many=False, context={"request": request})
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
            return Response({"detail": "SubCategory is deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "SubCategory does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    lang = openapi.Parameter('lang', in_=openapi.IN_QUERY, description='uz, en, ru', type=openapi.TYPE_STRING)
    ordering = openapi.Parameter(
        'ordering', in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='Enter field name to order for example: '
                    '"sub_cat_name" ascending; '
                    'put "-" for reverse ordering: "-sub_cat_name"'
    )

    @swagger_auto_schema(manual_parameters=[param_config, lang, ordering])
    def get(self, request):
        sub_category = SubCategory.objects.all()
        page = self.paginate_queryset(sub_category)
        lang = request.GET.get("lang")

        serializer = SubCatSerializer(page, many=True, context={"request": request})
        if page is not None:
            if lang == "uz":
                serializer = self.get_paginated_response(
                    SubCatSerializerUz(page, many=True, context={"request": request}).data)
            elif lang == "ru":
                serializer = self.get_paginated_response(
                    SubCatSerializerRu(page, many=True, context={"request": request}).data)
            elif lang == "en":
                serializer = self.get_paginated_response(
                    SubCatSerializerEn(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True, context={"request": request}).data)
        else:
            if lang == "uz":
                serializer = self.get_paginated_response(
                    SubCatSerializerUz(page, many=True, context={"request": request}).data)
            elif lang == "ru":
                serializer = self.get_paginated_response(
                    SubCatSerializerRu(page, many=True, context={"request": request}).data)
            elif lang == "en":
                serializer = self.get_paginated_response(
                    SubCatSerializerEn(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data,
                                                         context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleSubCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            sub_category = SubCategory.objects.get(id=pk)
            serializer = SubCatSerializer(sub_category, many=False, context={"request": request})
            return Response(serializer.data)
        except:
            return Response({"detail": "sub_category does not exist"})


class EquipmentAPI(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = EquipmentsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name', 'update_ts')
    ordering = ('id',)

    # search_fields = ['name', 'name_uz', 'name_ru', 'name_en']

    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config], request_body=EquipmentsSerializer,
                         parser_classes=parser_classes)
    def post(self, request):
        serializer = EquipmentsSerializer(data=request.data, many=False, context={"request": request})
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
        serializer = EquipmentsSerializer(equipment, many=False, data=request.data, context={"request": request})
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
            return Response({"detail": "equipment does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    lang = openapi.Parameter('lang', in_=openapi.IN_QUERY, description='uz, en, ru', type=openapi.TYPE_STRING)
    ordering = openapi.Parameter(
        'ordering', in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='Enter field name to order for example: '
                    '"equipment" ascending; '
                    'put "-" for reverse ordering: "-equipment"'
    )

    @swagger_auto_schema(manual_parameters=[param_config, lang, ordering])
    def get(self, request):
        equipment = Equipment.objects.all()
        page = self.paginate_queryset(equipment)
        lang = request.GET.get("lang")
        # filter = ProductFilter(request.GET, queryset=Product.objects.all())

        serializer = SubCatSerializer(equipment, many=True)
        if page is not None:
            if lang == "uz":
                serializer = self.get_paginated_response(
                    EquipmentsSerializerUz(page, many=True, context={"request": request}).data)
            elif lang == "ru":
                serializer = self.get_paginated_response(
                    EquipmentsSerializerRu(page, many=True, context={"request": request}).data)
            elif lang == "en":
                serializer = self.get_paginated_response(
                    EquipmentsSerializerEn(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True, context={"request": request}).data)
        else:
            if lang == "uz":
                serializer = self.get_paginated_response(
                    EquipmentsSerializerUz(page, many=True, context={"request": request}).data)
            elif lang == "ru":
                serializer = self.get_paginated_response(
                    EquipmentsSerializerRu(page, many=True, context={"request": request}).data)
            elif lang == "en":
                serializer = self.get_paginated_response(
                    EquipmentsSerializerEn(page, many=True, context={"request": request}).data)
            else:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True, context={"request": request}).data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.data, {'filter': filter}, status=status.HTTP_200_OK)


class SingleEquipment(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        try:
            equipment = Equipment.objects.get(id=pk)
            serializer = EquipmentsSerializer(equipment, many=False, context={"request": request})
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
    def post(self, request, parser_classes=parser_classes):
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
            return Response({"detail": "addition does not exist"}, status=status.HTTP_400_BAD_REQUEST)


#
class SingleAddition(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):

        """

        :param request:
        :param pk:
        :return:
        """
        try:
            addition = AdditionalProps.objects.get(id=pk)
            serializer = AdditionsSerializer(addition, many=False)
            return Response(serializer.data)
        except:
            return Response({"detail": "Addition does not exist"})


class SingleEquipmentAdditions(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    param_config = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
                                     description='enter access token with Bearer word for example: Bearer token',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request, pk):
        """

        :param request:
        :param pk:
        :return:
        """
        try:
            equipment = Equipment.objects.get(id=pk)
            additions = AdditionalProps.objects.filter(equipment=equipment)
            serializer = AdditionsSerializer(additions, many=True)
            return Response(serializer.data)
        except:
            return Response({"detail": "Additions does not exist"})


# ====================================WITHOUT TOKEN================================================================================

class CategoryGetOne(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name_uz', 'name_ru', 'name_en']
    search_fields = ["$name_uz", "$name_ru", "$name_en", ]
    pagination_class = LargeResultsSetPagination
    # malum biri
    # ordering_fields = ['username', 'email']
    # hammasi fieldlari kk bo'lsa'
    ordering_fields = '__all__'


class SubCategoryGetOne(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCatSerializer


class SubCategoryList(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCatSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name_uz', 'name_ru', 'name_en',"category"]
    search_fields = ["$name_uz", "$name_ru", "$name_en", ]
    pagination_class = LargeResultsSetPagination
    # malum biri
    # ordering_fields = ['username', 'email']
    # hammasi fieldlari kk bo'lsa'
    ordering_fields = '__all__'


class EquipmentGetOne(generics.RetrieveAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentsSerializer


class EquipmentList(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name_uz', 'name_ru', 'name_en',"sub_category","category"]
    search_fields = ["$name_uz", "$name_ru", "$name_en"]
    pagination_class = LargeResultsSetPagination
    # malum biri
    # ordering_fields = ['username', 'email']
    # hammasi fieldlari kk bo'lsa'
    ordering_fields = '__all__'
