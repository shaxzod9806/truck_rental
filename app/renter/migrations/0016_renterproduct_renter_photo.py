# Generated by Django 3.2.8 on 2022-02-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0015_auto_20220226_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='renterproduct',
            name='renter_photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/renters'),
        ),
    ]
