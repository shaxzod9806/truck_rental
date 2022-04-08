from rest_framework import serializers
from .models import Order, OrderChecking, FireBaseNotification, RefreshFireBaseToken
from customer.models import CustomerProfile
from index.models import User
from equipments.models import Equipment
from equipments.serializers import EquipmentsSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class FireBaseNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireBaseNotification
        fields = '__all__'


class RefreshFireBaseTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RefreshFireBaseToken
        fields = ['token', "fmc_token", "has_token", "users", "created_at", "updated_at"]

    def get_token(self, obj):
        token = AccessToken.for_user(obj)
        return str(token)


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField("get_customer_name")
    customer_phone = serializers.SerializerMethodField("get_customer_phone")
    customer_email = serializers.SerializerMethodField("get_customer_email")
    equipment_name = serializers.SerializerMethodField("get_equipment_name")
    status = serializers.SerializerMethodField(read_only=True)
    # equipment_image = serializers.SerializerMethodField("get_equipment_image")
    equipment_image_url = serializers.SerializerMethodField("get_equipment_image_url")
    renter_phone = serializers.SerializerMethodField("get_renter_phone")
    tip = serializers.SerializerMethodField("get_tip")
    hourly_price = serializers.SerializerMethodField("get_hourly_price")
    hourly_price_night = serializers.SerializerMethodField("get_hourly_price_night")

    def get_hourly_price(self, obj):
        request = self.context.get('request')
        # print(request.data)
        equipment = Equipment.objects.get(id=obj.equipment.id)
        # print(equipment)
        return equipment.hourly_price

    #
    def get_hourly_price_night(self, obj):
        request = self.context.get('request')
        equipment = Equipment.objects.get(id=obj.equipment.id)
        return equipment.hourly_price_night

    def get_tip(self, obj):
        request = self.context.get('request')
        equipment = Equipment.objects.get(id=obj.equipment.id)
        return equipment.tip

    # def get_tip(self, obj):
    #     request = self.context.get('request')
    #     equipment = Equipment.objects.get(id=obj.equipment.id)
    #     print(equipment)
    #     return equipment.tip

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
                  "equipment_image_url", "quantity", "tip", "hourly_price", "hourly_price_night",
                  "start_time", "end_time", "daylight_hours", "night_hours", "lat", "long", "address", "order_price",
                  "payment_type",
                  "user_cancel", "status", "customer_phone", "customer_email",
                  "notes", "created_at", "updated_at"
                  ]
