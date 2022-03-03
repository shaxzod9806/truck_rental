# Generated by Django 3.2.8 on 2022-02-25 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0013_renterproduct_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renterproduct',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]