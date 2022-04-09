from django.contrib import admin
from .models import CustomerProfile,Region,Country

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(Country)
admin.site.register(Region)
