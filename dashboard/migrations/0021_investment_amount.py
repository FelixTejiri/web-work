# Generated by Django 3.1 on 2020-09-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20200906_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]
