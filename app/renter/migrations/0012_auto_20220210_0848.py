# Generated by Django 3.2.8 on 2022-02-10 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0011_auto_20220210_0539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renterproduct',
            name='category',
        ),
        migrations.RemoveField(
            model_name='renterproduct',
            name='sub_category',
        ),
    ]