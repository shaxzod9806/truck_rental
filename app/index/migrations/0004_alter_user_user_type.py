# Generated by Django 3.2.8 on 2022-02-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_user_device_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'manager'), (3, 'renter'), (4, 'customer')], default=4),
        ),
    ]