from django.shortcuts import render
from .models import Order, OrderChecking
from index.models import User
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class OrderAPIView(APIView):
    permission_class = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = OrderSerializer

    param_config = openapi.Parameter(
        'Authorization',
        in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(request_body=OrderSerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def post(self, request):
        serializer = OrderSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order_id = openapi.Parameter(
        'order_id', in_=openapi.IN_FORM,
        description='enter order ID',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(request_body=OrderSerializer, parser_classes=parser_classes,
                         manual_parameters=[order_id, param_config])
    def put(self, request):
        order_id = request.data["order_id"]
        order = Order.objects.get(id=int(order_id))
        serializer = OrderSerializer(order, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[order_id, param_config])
    def delete(self, request):
        try:
            order = Order.objects.get(id=int(request.data['order_id']))
            order.delete()
            return Response({'detail': 'Order is deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[param_config])
    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class SingleBrandAPI(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = BrandSerializer
#     parser_classes = (MultiPartParser, FormParser)
#
#     token = openapi.Parameter('Authorization', in_=openapi.IN_HEADER,
#                               description='enter access token', type=openapi.TYPE_STRING, )
#
#     @swagger_auto_schema(manual_parameters=[token], parser_classes=parser_classes)
#     def get(self, request, pk):
#         try:
#             brand = Brand.objects.get(id=pk)
#             serializer = BrandSerializer(brand, many=False, context={"request": request})
#             return Response(serializer.data)
#         except:
#             return Response({'detail': 'Brand does not exist'})
