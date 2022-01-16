from django.db import models
from index.models import User
from equipments.models import Equipment

upload_path = 'renters/documents/'


class Profile(models.Model):
    organization = models.CharField(max_length=255, null=True)
    office_address = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    # files = models.ForeignKey(Files, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Files(models.Model):
    files = models.FileField(upload_to=upload_path)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)


class RenterProduct(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    renter_description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address_name = models.CharField(max_length=255)
    renter = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.equipment.name_uz


class BusyTimes(models.Model):
    #  busy_start should be greater than busy_end
    busy_start = models.DateTimeField()
    busy_end = models.DateTimeField()
    product = models.ForeignKey(RenterProduct, on_delete=models.CASCADE)




