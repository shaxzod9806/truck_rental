# Generated by Django 3.2.8 on 2022-03-30 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_customerprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='pochta_indexi',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]