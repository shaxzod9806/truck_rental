# Generated by Django 3.2.8 on 2022-03-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0019_auto_20220330_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='tip',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
