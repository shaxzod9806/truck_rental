# Generated by Django 3.2.8 on 2022-01-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_cancel',
            field=models.BooleanField(default=False),
        ),
    ]
