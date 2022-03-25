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
    # equipment_image = serializers.SerializerMethodField("get_equipment_image")
    equipment_image_url = serializers.SerializerMethodField("get_equipment_image_url")
    renter_phone = serializers.SerializerMethodField("get_renter_phone")

    def get_equipment_image_url(self, obj):
        request = self.context.get('request')
        equipment = Equipment.objects.get(id=obj.equipment.id)
        photo_url = equipment.image.url
        return request.build_absolute_uri(photo_url)

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
        request = self.context.get('request')
        lang = request.GET.get('lang')
        print(lang)
        if lang == 'uz':
            return equipment.name_uz
        elif lang == 'ru':
            return equipment.name_ru
        elif lang == 'en':
            return equipment.name_en
        else:
            return equipment.name_ru

    def get_status(self, obj):
        request = self.context.get('request')
        status = 1
        if request.method == 'GET':
            status = OrderChecking.objects.get(order=obj).confirmed
        return status

    def get_renter_phone(self, obj):
        try:
            request = self.context.get('request')
            renter_phone = User.objects.get(id=obj.renter.id).username
            return renter_phone
        except:
            return None

    class Meta:
        model = Order
        fields = ["id", "customer", 'customer_name', "renter", "renter_phone", "equipment", "equipment_name",
                  "equipment_image_url", "quantity",
                  "start_time", "end_time", "lat", "long", "address", "order_price","payment_type",
                  "user_cancel", "status", "customer_phone", "customer_email",
                  "notes", "created_at", "updated_at"
                  ]
