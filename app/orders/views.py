from django.shortcuts import render
from .models import Order, OrderChecking
from index.models import User
from equipments import Equipment
from .serializers import OrderSerializer
from rest_framework.views import APIView

# Create your views here.

class OrderApi(APIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER,
        description='enter access token with Bearer word for example: Bearer token',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[param_config], )
    def get(self, request):
        order = request.order
        # user_serializer = UserSerializer(user, many=True)
        order_serializer = OrderSerializer(order, many=True)
        # data = {"user": user_serializer.data, "user_profile": customer_serializer.data}
        return Response(order_serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def post(self, request):
        serializer = OrderSerializer(data=request.data, many=False,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=OrderSerializer, parser_classes=parser_classes,
                         manual_parameters=[param_config])
    def put(self, request):
        serializer = OrderSerializer(brand, many=False, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[param_config])
    def delete(self, request):
        try:
            brand = Brand.objects.get(id=int(request.data['brand_id']))
            brand.delete()
            return Response({'detail': 'Brand is deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Brand does not exist'}, status=status.HTTP_400_BAD_REQUEST)




