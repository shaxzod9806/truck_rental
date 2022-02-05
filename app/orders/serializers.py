from rest_framework import serializers
from .models import Order, OrderChecking
from customer.models import CustomerProfile
from index.models import User
from equipments.models import Equipment


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField("get_customer_name")
    customer_phone = serializers.SerializerMethodField("get_customer_phone")
    customer_email = serializers.SerializerMethodField("get_customer_email")
    equipment_name = serializers.SerializerMethodField("get_equipment_name")
    status = serializers.SerializerMethodField(read_only=True)


    def get_customer_name(self, obj):
        user = User.objects.get(id=obj.customer.id)
        return user.first_name

    def get_customer_phone(self, obj):
        user = User.objects.get(id=obj.customer.id)
        return user.username

    def get_customer_email(self, obj):
        user = User.objects.get(id=obj.customer.id)
        return user.email

    def get_equipment_name(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        return equipment.name_ru

    def get_status(self, obj):
        request = self.context.get('request')
        status = "pending"
        if request.method == 'GET':
            status = OrderChecking.objects.get(order=obj).confirmed
        return status

    class Meta:
        model = Order
        fields = ["id","customer", 'customer_name', "equipment", "equipment_name",
                  "start_time", "end_time", "lat", "long", "address", "order_price",
                  "user_cancel", "status", "customer_phone", "customer_email",
                  "notes", "created_at", "updated_at"]
