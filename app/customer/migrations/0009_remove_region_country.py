# Generated by Django 3.2.8 on 2022-01-29 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20220129_0817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='country',
        ),
    ]
