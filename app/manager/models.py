from django.db import models
from index.models import User

# Create your models here.
class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics',null=True,blank=True)
    bio = models.TextField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.user.username
