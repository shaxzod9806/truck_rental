from django.db import models
from index.models import User


# Create your models here.


class CustomerProfile(models.Model):
    phone_number = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number
