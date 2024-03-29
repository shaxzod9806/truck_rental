# Generated by Django 3.2.8 on 2022-01-29 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_remove_region_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.country'),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.region'),
        ),
    ]
