# Generated by Django 3.2.8 on 2022-03-03 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0016_auto_20220303_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalprops',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='additionalprops',
            name='value_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]