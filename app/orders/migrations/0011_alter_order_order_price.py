# Generated by Django 3.2.8 on 2022-01-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_renter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_price',
            field=models.FloatField(null=True),
        ),
    ]
