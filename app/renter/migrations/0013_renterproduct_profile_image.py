# Generated by Django 3.2.8 on 2022-02-25 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0012_auto_20220210_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='renterproduct',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]
