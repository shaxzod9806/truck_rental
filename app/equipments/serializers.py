from rest_framework import serializers
from .models import Category, SubCategory, Equipment, AdditionalProps


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class EquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class AdditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProps
        fields = "__all__"


