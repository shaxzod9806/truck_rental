from rest_framework import serializers
from index.models import User
from .models import Profile, Files, RenterProduct
from rest_framework_simplejwt.tokens import AccessToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id','is_active', 'username', 'email', 'first_name', 'last_name', 'user_type', 'token')

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
        return obj.country.country_name

    def get_region_name(self, obj):
        return obj.region.region_name


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('files', 'profile')


class RenterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterProduct
        fields = "__all__"
