from rest_framework import serializers
from .models import ManagerProfile


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = ('id',"user","image","bio")


