# Generated by Django 3.2.8 on 2022-01-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='start_time',
            field=models.DateTimeField(blank=True),
        ),
    ]