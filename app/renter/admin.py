from django.contrib import admin
from .models import Profile, Files, RenterProduct
from index.models import User

# Register your models here.

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Files)
admin.site.register(RenterProduct)
