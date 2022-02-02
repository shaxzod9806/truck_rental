from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'manager'),
        (3, 'renter'),
        (4, 'customer'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)
    activation_code = models.IntegerField(null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True)
