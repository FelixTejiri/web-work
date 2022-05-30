# Generated by Django 3.1 on 2020-08-12 01:13

import dashboard.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20200812_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='expiration_date',
            field=models.DateTimeField(default=dashboard.models.Investment.get_expiration_time),
        ),
        migrations.AddField(
            model_name='investment',
            name='is_active',
            field=models.BooleanField(choices=[('Active', True), ('Inactive', False)], default=False),
        ),
        migrations.AddField(
            model_name='proofofpayment',
            name='is_valid',
            field=models.IntegerField(choices=[('Pending', 1), ('Invalid', 2), ('Valid', 3)], default=1),
        ),
        migrations.AlterField(
            model_name='investment',
            name='activation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
