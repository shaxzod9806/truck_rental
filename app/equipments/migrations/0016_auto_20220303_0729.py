# Generated by Django 3.2.8 on 2022-03-03 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0015_auto_20220223_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='image',
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
