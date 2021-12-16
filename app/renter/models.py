from django.db import models
from index.models import User

upload_path = 'renters/documents/'


class Profile(models.Model):
    phone_number = models.CharField(max_length=255, null=True)
    organization = models.CharField(max_length=255, null=True)
    office_address = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    # files = models.ForeignKey(Files, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Files(models.Model):
    files = models.FileField(upload_to=upload_path)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
