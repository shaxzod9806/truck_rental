# Generated by Django 3.2.8 on 2021-12-07 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0004_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='brand_image',
            field=models.ImageField(null=True, upload_to='equipments/brands'),
        ),
    ]
