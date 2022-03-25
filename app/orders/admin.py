from django.contrib import admin
from .models import Order, OrderChecking

# Register your models here.
admin.site.register(Order)


# admin.site.register(OrderChecking)
@admin.register(OrderChecking)
class OrderCheckingAdmin(admin.ModelAdmin):
    # list_editable = ['renter', 'equipment', 'order',  'checking_end', 'confirmed']
    fields = ('renter', 'equipment', 'order', 'checking_end', 'confirmed'
              )
    list_display = ('id', 'renter', 'equipment', 'order', 'confirmed', 'checking_start', 'checking_end',
                    )
    list_filter = ('renter', 'equipment', 'order', 'checking_start', 'checking_end', 'confirmed',)
    search_fields = ('renter__renter', 'equipment__equipment', 'order__order',)
    ordering = ('renter', 'equipment', 'order', 'checking_start', 'checking_end', 'confirmed',)
