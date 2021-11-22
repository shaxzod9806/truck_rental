from django.db import models
from index.models import User
# Create your models here.
upload_path = 'equipments/'


class Category(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
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
    name_en = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_path, null=True)
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


class Equipment(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_path)
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


class AdditionalProps(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    value_uz = models.CharField(max_length=255)
    value_ru = models.CharField(max_length=255)
    value_en = models.CharField(max_length=255)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)









