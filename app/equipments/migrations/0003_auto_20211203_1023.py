# Generated by Django 3.2.8 on 2021-12-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ru',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description_uz',
            field=models.TextField(blank=True),
        ),
    ]