# Generated by Django 3.2.8 on 2022-03-30 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_customerprofile_customer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'erkak'), (2, 'ayol')], null=True),
        ),
    ]
