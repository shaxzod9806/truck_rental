from django.contrib import admin
from .models import Category, Equipment, AdditionalProps, SubCategory,\
Brand

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(AdditionalProps)
admin.site.register(Equipment)
admin.site.register(Brand)

