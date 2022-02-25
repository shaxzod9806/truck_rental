from rest_framework import serializers
from index.models import User
from equipments.models import Equipment, Category, SubCategory
from customer.models import Region, Country
from .models import Profile, Files, RenterProduct
from rest_framework_simplejwt.tokens import AccessToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'device_id', 'is_active', 'username', 'email', 'first_name', 'last_name', 'user_type', 'token')

    def get_token(self, obj):
        token = AccessToken.for_user(obj)
        return str(token)


class ProfileSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField("get_country_name")
    region_name = serializers.SerializerMethodField("get_region_name")

    class Meta:
        model = Profile
        fields = ["id", "organization", "office_address", "user", "country", "country_name", "region", "region_name"]

    def get_country_name(self, obj):
        country = Country.objects.get(id=obj.country_id)
        return country.country_name

    def get_region_name(self, obj):
        region = Region.objects.get(id=obj.region_id)
        return region.region_name


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('files', 'profile')


class RenterProductSerializer(serializers.ModelSerializer):
    equipment_name = serializers.SerializerMethodField("get_equipment_name")
    renter_name = serializers.SerializerMethodField("get_renter_name")
    category_id = serializers.SerializerMethodField("get_category_id")
    category_name = serializers.SerializerMethodField("get_category_name")
    sub_category_id = serializers.SerializerMethodField("get_sub_category_id")
    sub_category_name = serializers.SerializerMethodField("get_sub_category_name")

    def get_category_id(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        category = Category.objects.get(id=equipment.category.id)
        return category.id

    def get_category_name(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        category = Category.objects.get(id=equipment.category.id)
        return category.name_ru

    def get_sub_category_name(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        sub_category = SubCategory.objects.get(id=equipment.sub_category.id)
        return sub_category.name_ru

    def get_sub_category_id(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        sub_category = SubCategory.objects.get(id=equipment.sub_category.id)
        return sub_category.id

    def get_equipment_name(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        return equipment.name_ru

    def get_renter_name(self, obj):
        profile = Profile.objects.get(id=obj.renter.id)
        user = User.objects.get(id=profile.user.id)
        return user.first_name

    class Meta:
        model = RenterProduct
        fields = ["id", "category_id", "category_name", "sub_category_id", "sub_category_name",
                  "equipment", "equipment_name", "renter_description", "latitude", "longitude",
                  "address_name", "renter", "renter_name"]
