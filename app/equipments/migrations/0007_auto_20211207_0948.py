# Generated by Django 3.2.8 on 2021-12-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0006_equipment_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='description_en',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description_ru',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description_uz',
            field=models.TextField(blank=True),
        ),
    ]