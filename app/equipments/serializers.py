import django_filters
from rest_framework import serializers

from .models import Category, SubCategory, Equipment, AdditionalProps, \
    Brand


class BrandSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField

    class Meta:
        model = Brand
        fields = ('id', 'brand_name', 'brand_image', 'created_at', 'updated_at')

        def get_photo_url(self, obj):
            request = self.context.get('request')
            photo_url = obj.image.url
            return request.build_absolute_url(photo_url)


class EquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = Equipment
        fields = ['name_uz']


class CategorySerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField

    class Meta:
        model = Category
        fields = "__all__"

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_url(photo_url)


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
    photo_url = serializers.SerializerMethodField('get_photo_url')
    category_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_ru

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)

    class Meta:
        model = SubCategory
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image', 'description_uz', 'description_ru', 'description_en',
                  'photo_url',
                  'category_name',
                  'category', 'created_at', 'updated_at',
                  'created_by', 'updated_by']


class SubCatSerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')
    description = serializers.SerializerMethodField('description_uz')
    category_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_uz

    def description_uz(self, obj):
        description = obj.description_uz
        return description

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'image', 'category', 'category_name', 'created_at', 'updated_at',
                  'created_by',
                  'updated_by']


class SubCatSerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')
    description = serializers.SerializerMethodField('description_ru')
    category_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_ru

    def description_ru(self, obj):
        description = obj.description_ru
        return description

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'image', 'category', 'category_name',
                  'created_at', 'updated_at',
                  'created_by',
                  'updated_by']


class SubCatSerializerEn(serializers.ModelSerializer):
    description = serializers.SerializerMethodField('description_en')
    name = serializers.SerializerMethodField('name_en')
    category_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_en

    def description_en(self, obj):
        description = obj.description_en
        return description

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'image', 'category', 'category_name', 'created_at', 'updated_at',
                  'created_by',
                  'updated_by']


class EquipmentsSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField('get_photo_url')
    category_name = serializers.SerializerMethodField('get_category_name')
    sub_category_name = serializers.SerializerMethodField('get_sub_category_name')
    brand_name = serializers.SerializerMethodField('get_brand_name')

    def get_brand_name(self, obj):
        brand = Brand.objects.get(id=obj.brand.id)
        return brand.brand_name

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_ru

    def get_sub_category_name(self, obj):
        sub_cat = SubCategory.objects.get(id=obj.sub_category.id)
        return sub_cat.name_ru

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)

    class Meta:
        model = Equipment
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image', 'photo_url',
                  'brand', 'brand_name',
                  'category_name', 'category', 'sub_category_name', 'sub_category',
                  'created_at', 'updated_at', 'created_by', 'updated_by', 'hourly_price', "hourly_price_night"]


class EquipmentsSerializerUz(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_uz')
    category_name = serializers.SerializerMethodField('get_category_name')
    sub_category_name = serializers.SerializerMethodField('get_sub_category_name')
    description = serializers.SerializerMethodField('description_uz')

    def description_en(self, obj):
        description = obj.description_uz
        return description

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_uz

    def get_sub_category_name(self, obj):
        sub_cat = SubCategory.objects.get(id=obj.sub_category.id)
        return sub_cat.name_uz

    def name_uz(self, obj):
        name = obj.name_uz
        return name

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'image', 'category', 'category_name', 'sub_category',
                  'sub_category_name', 'created_at',
                  'updated_at',
                  'created_by',
                  'updated_by']


class EquipmentsSerializerRu(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_ru')
    category_name = serializers.SerializerMethodField('get_category_name')
    sub_category_name = serializers.SerializerMethodField('get_sub_category_name')
    description = serializers.SerializerMethodField('description_ru')

    def description_ru(self, obj):
        description = obj.description_en
        return description

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_ru

    def get_sub_category_name(self, obj):
        sub_cat = SubCategory.objects.get(id=obj.sub_category.id)
        return sub_cat.name_ru

    def name_ru(self, obj):
        name = obj.name_ru
        return name

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'image', 'category',
                  'category_name', 'sub_category', 'sub_category_name', 'created_at', 'updated_at', 'created_by',
                  'updated_by']


class EquipmentsSerializerEn(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_en')
    category_name = serializers.SerializerMethodField('get_category_name')
    sub_category_name = serializers.SerializerMethodField('get_sub_category_name')
    description = serializers.SerializerMethodField('description_en')

    def description_en(self, obj):
        description = obj.description_en
        return description

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name_en

    def get_sub_category_name(self, obj):
        sub_cat = SubCategory.objects.get(id=obj.sub_category.id)
        return sub_cat.name_en

    def name_en(self, obj):
        name = obj.name_en
        return name

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'image', 'category_name', 'category', 'sub_category',
                  'sub_category_name', 'created_at',
                  'updated_at', 'created_by',
                  'updated_by']


class AdditionsSerializer(serializers.ModelSerializer):
    equipment_name = serializers.SerializerMethodField('get_equipment_name')

    def get_equipment_name(self, obj):
        equipment = Equipment.objects.get(id=obj.equipment.id)
        return equipment.name_ru

    class Meta:
        model = AdditionalProps

        fields = ("id", "name_uz", "name_ru", "name_en", 'value_uz', 'value_ru', 'value_en',
                  'equipment', 'equipment_name', 'created_at', 'updated_at')
