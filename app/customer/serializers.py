from rest_framework import serializers
from .models import CustomerProfile, Country, Region
# from index.models import User
from index.models import User


class CustomerSerializer(serializers.ModelSerializer):
    # users = UserSerializer(many=True)
    country_name = serializers.SerializerMethodField("get_country_name")
    region_name = serializers.SerializerMethodField("get_region_name")
    photo_url = serializers.SerializerMethodField("get_image_url")

    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_user_last_name')

    def get_first_name(self, obj):
        try:
            usr = User.objects.get(id=obj.user.id)
            return usr.first_name
        except:
            return ""

    def get_user_last_name(self, obj):
        try:
            usr = User.objects.get(id=obj.user.id)
            return usr.last_name
        except:
            return ""

    class Meta:
        model = CustomerProfile
        fields = ("id",
                  "phone_number", "customer_image", "photo_url", "customer_address", "first_name", "last_name",
                  "gender", "user", "country",
                  "country_name",
                  "region",
                  "region_name", "pochta_indexi")

    # def get_first_name(self, obj):
    #     request = self.context.get("request")
    #     if request.method == "PUT":
    #         return obj.user.first_name
    #     return ""

    def get_image_url(self, obj):
        try:
            request = self.context.get("request")
            photo_url = obj.customer_image.url
            return request.build_absolute_uri(photo_url)
        except:
            return ""

    def get_country_name(self, obj):
        try:
            country = Country.objects.get(id=obj.country.id)
            return country.country_name
        except:
            return null

    def get_region_name(self, obj):
        try:
            region = Region.objects.get(id=obj.region.id)
            return region.region_name
        except:
            return null


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField("get_country_name")

    class Meta:
        model = Region
        fields = ["id", "region_name", "country", "country_name"]

    def get_country_name(self, obj):
        return obj.country.country_name
