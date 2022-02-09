from rest_framework import serializers
from index.models import User
from equipments.models import Equipment
from customer.models import Region, Country
from .models import Profile, Files, RenterProduct
from rest_framework_simplejwt.tokens import AccessToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'is_active', 'username', 'email', 'first_name', 'last_name', 'user_type', 'token')

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
        country = Country.objects.get(id=obj.country.id)
        return country.country_name

    def get_region_name(self, obj):
        region = Region.objects.get(id=obj.region.id)
        return region.region_name


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('files', 'profile')


class RenterProductSerializer(serializers.ModelSerializer):
    equipment_name = serializers.SerializerMethodField("get_equipment_name")
    renter_name = serializers.SerializerMethodField("get_renter_name")

    def get_equipment_name(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        return equipment.name_ru

    def get_renter_name(self, obj):
        profile = Profile.objects.get(id=obj.renter.id)
        user = User.objects.get(id=profile.user.id)
        return user.first_name

    class Meta:
        model = RenterProduct
        fields = ["id", "equipment", "equip"
                                     "ment_name", "renter_description", "latitude", "longitude",
                  "address_name", "renter", "renter_name"]
