from django.db import models
from index.models import User
# Create your models here.


class CustomerProfile(models.Model):
    phone_number = models.CharField(max_length=13)
    customer_addresss = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
