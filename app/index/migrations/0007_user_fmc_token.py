# Generated by Django 3.2.8 on 2022-04-12 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_remove_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fmc_token',
            field=models.TextField(blank=True, default='string', null=True),
        ),
    ]
