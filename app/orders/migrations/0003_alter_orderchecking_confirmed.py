# <<<<<<< HEAD
# Generated by Django 3.2.8 on 2022-04-14 16:15
# =======
# Generated by Django 3.2.8 on 2022-04-15 19:20
# >>>>>>> 9055693ac7e53143e95936b4c9298dc33023f1df

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderchecking_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderchecking',
            name='confirmed',
            field=models.SmallIntegerField(choices=[(1, 'pending'), (2, 'canceled'), (3, 'accepted'), (4, 'no response')]),
        ),
    ]