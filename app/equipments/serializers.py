from rest_framework import serializers
from .models import Category, SubCategory, Equipment, AdditionalProps


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategorySerializerUz(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CategorySerializerRu(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CategorySerializerEn(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_en', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


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


