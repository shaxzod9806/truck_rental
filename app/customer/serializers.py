from rest_framework import serializers
from .models import CustomerProfile, Country, Region


class CustomerSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField("get_country_name")
    region_name = serializers.SerializerMethodField("get_region_name")

    class Meta:
        model = CustomerProfile
        fields = ("phone_number", "customer_address", "user", "country", "country_name", "region", "region_name")

    def get_country_name(self, obj):
        return obj.country.country_name

    def get_region_name(self, obj):
        return obj.region.region_name


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
