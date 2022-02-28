from rest_framework import serializers
from .models import CustomerProfile, Country, Region


class CustomerSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField("get_country_name")
    region_name = serializers.SerializerMethodField("get_region_name")
    photo_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = CustomerProfile
        fields = (
            "phone_number", "customer_image", "photo_url", "customer_address", "user", "country", "country_name",
            "region",
            "region_name")

    def get_image_url(self, obj):
        request = self.context.get("request")
        print(request)
        photo_url = obj.customer_image.url
        return request.build_absolute_uri(photo_url)

    def get_country_name(self, obj):
        country = Country.objects.get(id=obj.country.id)
        return country.country_name

    def get_region_name(self, obj):
        region = Region.objects.get(id=obj.region.id)
        return region.region_name


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
