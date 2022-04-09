from django.db import models
from index.models import User
from equipments.models import Equipment, Category, SubCategory
from customer.models import Region, Country

upload_path = "equipments/"
upload_path_image = 'users/renters'


class Profile(models.Model):
    TYPE_CHOISE_GENDER = (
        (1, "erkak"),
        (2, "ayol"),
    )

    gender = models.PositiveSmallIntegerField(choices=TYPE_CHOISE_GENDER, null=True, blank=True)
    pochta_indexi = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True)
    office_address = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profile_image = models.ImageField(upload_to=upload_path_image, null=True, blank=True)

    # files = models.ForeignKey(Files, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Files(models.Model):
    files = models.FileField(upload_to=upload_path)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)


class RenterProduct(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    # sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    renter_description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address_name = models.CharField(max_length=255)
    renter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    renter_photo = models.ImageField(upload_to=upload_path_image, null=True, blank=True)

    def __str__(self):
        return self.equipment.name_uz


class BusyTimes(models.Model):
    #  busy_start should be greater than busy_end
    busy_start = models.DateTimeField()
    busy_end = models.DateTimeField()
    product = models.ForeignKey(RenterProduct, on_delete=models.CASCADE)
