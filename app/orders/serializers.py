from rest_framework import serializers
from .models import Order, OrderChecking


class OrderSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        request = self.context.get('request')
        status = "pending"
        if request.method == 'GET':
            status = OrderChecking.objects.get(order=obj).confirmed
        return status

    class Meta:
        model = Order
        fields = "__all__"

