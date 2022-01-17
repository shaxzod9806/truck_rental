# Generated by Django 3.2.8 on 2022-01-06 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0011_auto_20211213_1510'),
        ('renter', '0002_auto_20211214_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenterProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hourly_price', models.FloatField()),
                ('renter_description', models.TextField(blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address_name', models.CharField(max_length=255)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.equipment')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='renter.profile')),
            ],
        ),
    ]
