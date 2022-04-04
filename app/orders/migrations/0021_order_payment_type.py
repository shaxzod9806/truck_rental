# Generated by Django 3.2.8 on 2022-03-25 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.IntegerField(choices=[(1, 'CLICK'), (2, 'PAY_ME'), (3, 'NAQD_PUL'), (4, 'BANK_ORQALI')], default=3),
        ),
    ]