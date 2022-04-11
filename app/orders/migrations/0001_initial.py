# Generated by Django 3.2.8 on 2022-04-11 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('renter', '0017_auto_20220401_0603'),
        ('equipments', '0021_auto_20220401_0603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('night_hours', models.FloatField(blank=True, null=True)),
                ('daylight_hours', models.FloatField(blank=True, null=True)),
                ('lat', models.CharField(max_length=255, null=True)),
                ('long', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('order_price', models.FloatField(null=True)),
                ('payment_type', models.IntegerField(choices=[(1, 'CLICK'), (2, 'PAY_ME'), (3, 'APELSIN')], default=1)),
                ('user_cancel', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='equipment', to='equipments.equipment')),
                ('renter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='renter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RefreshFireBaseToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fmc_token', models.TextField(blank=True, null=True)),
                ('has_token', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderChecking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checking_start', models.DateTimeField(auto_now_add=True)),
                ('checking_end', models.DateTimeField()),
                ('confirmed', models.CharField(choices=[(1, 'pending'), (2, 'canceled'), (3, 'accepted'), (4, 'no response')], max_length=255)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='renter.renterproduct')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.order')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renter_temp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FireBaseNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('type_notification', models.IntegerField(choices=[(1, 'ACCEPTED'), (2, 'CANCELED'), (3, 'NO_RESPONSE')], default=3)),
                ('oreder_id', models.IntegerField(blank=True, default=None, null=True)),
                ('image_url', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
