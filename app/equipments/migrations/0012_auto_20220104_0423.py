# Generated by Django 3.2.8 on 2022-01-04 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0011_auto_20211213_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalprops',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.equipment'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='image',
            field=models.ImageField(null=True, upload_to='equipments/'),
        ),
    ]
