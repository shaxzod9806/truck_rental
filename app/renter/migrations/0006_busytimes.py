# Generated by Django 3.2.8 on 2022-01-16 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0005_remove_renterproduct_hourly_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusyTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('busy_start', models.DateTimeField()),
                ('busy_end', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='renter.renterproduct')),
            ],
        ),
    ]
