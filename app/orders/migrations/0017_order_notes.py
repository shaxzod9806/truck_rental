# Generated by Django 3.2.8 on 2022-02-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_alter_orderchecking_renter'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]