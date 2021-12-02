from rest_framework import serializers
from .models import Category, SubCategory, Equipment, AdditionalProps


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategorySerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CategorySerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CategorySerializerEn(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_en')

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class SubCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class SubCatSerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class SubCatSerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class SubCatSerializerEn(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_en')

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class EquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class AdditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProps
        fields = "__all__"
