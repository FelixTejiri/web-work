# Generated by Django 3.1 on 2020-09-07 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0010_auto_20200907_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmentplan',
            old_name='second_payment_day',
            new_name='second_payment_date',
        ),
    ]
