from django.db import models
from index.models import User

# Create your models here.
upload_path = 'equipments/'
upload_path_brand = 'equipments/brands'


class Brand(models.Model):
    brand_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    status = models.BooleanField(default=True)
    brand_image = models.ImageField(upload_to=upload_path_brand, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='categories_created',
                                   related_query_name='categories_created'
                                   )
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='categories_updated',
                                   related_query_name='categories_updated'
                                   )

    def __str__(self):
        return self.name_ru


class SubCategory(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(null=True, blank=True)
    # image = models.ImageField(upload_to=upload_path, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='sub_cat_created',
                                   related_query_name='sub_cat_created'
                                   )
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='sub_cat_updated',
                                   related_query_name='sub_cat_updated'
                                   )

    def __str__(self):
        return self.name_ru


# quantity to order
class Equipment(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(null=True, blank=True)
    hourly_price = models.FloatField(null=True)
    hourly_price_night = models.FloatField(null=True)
    tip = models.CharField(max_length=255, null=True)
    gabarity_mm = models.CharField(max_length=255, null=True)
    ves = models.CharField(max_length=255, null=True)
    moshnost_kvt = models.CharField(max_length=255, null=True)
    shirina_ukladki = models.CharField(max_length=255, null=True)
    tolshina_ukladki = models.CharField(max_length=255, null=True)
    skorost_ukladki = models.CharField(max_length=255, null=True)
    skorost_dvizheniya = models.CharField(max_length=255, null=True)
    zagruzka_bunker = models.CharField(max_length=255, null=True)

    image = models.ImageField(upload_to=upload_path, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='equipments_created',
                                   related_query_name='equipment_created'
                                   )
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='equipments_updated',
                                   related_query_name='equipment_updated'
                                   )

    def __str__(self):
        return self.name_ru or "no name ru"


class AdditionalProps(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    value_uz = models.CharField(max_length=255)
    value_ru = models.CharField(max_length=255)
    value_en = models.CharField(max_length=255, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_ru
