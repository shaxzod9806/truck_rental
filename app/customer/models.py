from django.db import models
from index.models import User

upload_path = 'users'


# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.country_name


class Region(models.Model):
    region_name = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.region_name


class CustomerProfile(models.Model):
    TYPE_CHOISE_GENDER = (
        (1, "erkak"),
        (2, "ayol"),
    )
    phone_number = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)
    customer_address = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='users')
    customer_image = models.ImageField(upload_to=upload_path, null=True)
    gender = models.PositiveSmallIntegerField(choices=TYPE_CHOISE_GENDER, null=True, blank=True)
    pochta_indexi = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.phone_number
