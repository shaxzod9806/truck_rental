from django.db import models
from index.models import User


class Profile(models.Model):
    phone_number = models.CharField(max_length=255, null=True)
    organization = models.CharField(max_length=255, null=True)
    office_address = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


