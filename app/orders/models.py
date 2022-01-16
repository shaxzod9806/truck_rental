from django.db import models
from index.models import User
from equipments.models import Equipment
# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="customer")
    renter = models.ForeignKey(User, on_delete=models.PROTECT, related_name="renter")
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    lat = models.CharField(max_length=255)
    long = models.CharField(max_length=255)
    order_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


order_status = (
        (1, 'pending'),
        (2, 'canceled'),
        (3, 'accepted'),
        (4, 'no response'),
    )


class OrderChecking(models.Model):
    renter = models.ForeignKey(User, on_delete=models.PROTECT, related_name="renter_temp")
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    oder = models.ForeignKey(Order, on_delete=models.PROTECT)
    checking_start = models.DateTimeField(auto_now_add=True)
    checking_end = models.DateTimeField()
    confirmed = models.IntegerField(choices=order_status)

