from rest_framework import serializers
from .models import CustomerProfile


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
