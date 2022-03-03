from django.db import models
from index.models import User
from equipments.models import Equipment
from renter.models import RenterProduct


# Create your models here.

class Order(models.Model):
    # User  -> customer profile
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer", null=True)  #
    renter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="renter", blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, null=True)
    quantity = models.IntegerField(default=1)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    order_price = models.FloatField(null=True)
    user_cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)


order_status = (
    (1, 'pending'),
    (2, 'canceled'),
    (3, 'accepted'),
    (4, 'no response'),
)


class OrderChecking(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renter_temp")
    equipment = models.ForeignKey(RenterProduct, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    checking_start = models.DateTimeField(auto_now_add=True)
    checking_end = models.DateTimeField()
    confirmed = models.CharField(max_length=255, choices=order_status)
