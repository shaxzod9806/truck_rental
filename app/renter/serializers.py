from rest_framework import serializers
from index.models import User
from .models import Profile, Files
from rest_framework_simplejwt.tokens import AccessToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'token']

    def get_token(self, obj):
        token = AccessToken.for_user(obj)
        return str(token)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('files', 'profile')
