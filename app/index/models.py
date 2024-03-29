from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

upload_path = 'users'
upload_image_path = 'users/images/'


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
    fmc_token = models.TextField(null=True, blank=True, default="string")
    fmc_token_updated_time = models.DateTimeField(auto_now=True)
