# Generated by Django 3.2.8 on 2022-02-23 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0014_equipment_hourly_price_night'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
