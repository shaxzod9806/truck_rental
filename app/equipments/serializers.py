from rest_framework import serializers
from .models import Category, SubCategory, Equipment, AdditionalProps, \
    Brand
import django_filters


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'



class EquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = Equipment
        fields = ['name_uz']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategorySerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')
    description = serializers.SerializerMethodField('description_uz')

    def description_uz(self, obj):
        description = obj.description_uz
        return description

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CategorySerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')
    description = serializers.SerializerMethodField('description_ru')

    def description_ru(self, obj):
        description = obj.description_ru
        return description

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CategorySerializerEn(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_en')
    description = serializers.SerializerMethodField('description_en')

    def description_en(self, obj):
        description = obj.description_en
        return description

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'created_by', 'updated_by']


class SubCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class SubCatSerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')
    description = serializers.SerializerMethodField('description_uz')

    def description_uz(self, obj):
        description = obj.description_uz
        return description

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'image', 'category', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class SubCatSerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')
    description = serializers.SerializerMethodField('description_ru')

    def description_ru(self, obj):
        description = obj.description_ru
        return description

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'image', 'category', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class SubCatSerializerEn(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_en')

    def description_en(self, obj):
        description = obj.description_en
        return description

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'image', 'category', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class EquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class EquipmentsSerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'image', 'category', 'sub_category', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class EquipmentsSerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'image', 'category', 'sub_category', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class EquipmentsSerializerEn(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_en')

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'image', 'category', 'sub_category', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class AdditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProps
        fields = "__all__"
