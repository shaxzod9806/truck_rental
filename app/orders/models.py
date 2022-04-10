from django.db import models
from index.models import User
from equipments.models import Equipment
from renter.models import RenterProduct


# Create your models here.

class Order(models.Model):
    TYPE_CHOICES = (
        (1, 'CLICK'),
        (2, 'PAY_ME'),
        (3, 'APELSIN'),

    )
    # User  -> customer profile
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer", null=True)  #
    renter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="renter", blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name="equipment", null=True, )
    quantity = models.IntegerField(default=1)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    night_hours = models.FloatField(null=True, blank=True)
    daylight_hours = models.FloatField(null=True, blank=True)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    order_price = models.FloatField(null=True)
    payment_type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    user_cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=False)


class OrderChecking(models.Model):
    order_status = (
        (1, 'pending'),
        (2, 'canceled'),
        (3, 'accepted'),
        (4, 'no response'),
    )

    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renter_temp")
    equipment = models.ForeignKey(RenterProduct, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    checking_start = models.DateTimeField(auto_now_add=True)
    checking_end = models.DateTimeField()
    confirmed = models.CharField(max_length=255, choices=order_status)


class FireBaseNotification(models.Model):
    TYPE_CHOICES = (
        (1, 'ACCEPTED'),
        (2, 'CANCELED'),
        (3, 'NO_RESPONSE'),
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type_notification = models.IntegerField(choices=TYPE_CHOICES, default=3)
    oreder_id = models.IntegerField(null=True)
    image_url = models.CharField(max_length=255, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RefreshFireBaseToken(models.Model):
    fmc_token = models.TextField(null=True, blank=True)
    has_token = models.BooleanField(default=False)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
