from django.contrib import admin
from .models import Profile, Files, RenterProduct
from index.models import User

# Register your models here.

admin.site.register(Profile)
# admin.site.register(User)
admin.site.register(Files)
admin.site.register(RenterProduct)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('is_active',  'username', 'email', 'first_name', 'last_name', 'user_type','device_id','activation_code'
              )
    list_display = ('id', 'user_type', 'is_active',  'username', 'email', 'first_name', 'last_name','device_id','activation_code'
                    )
    list_filter = ( 'is_active', 'user_type',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    ordering = ('username', 'first_name', 'last_name', 'email',)
