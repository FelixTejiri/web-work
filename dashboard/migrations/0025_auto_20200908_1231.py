# Generated by Django 3.1 on 2020-09-08 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_auto_20200907_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Paid'), (2, 'Unpaid'), (3, 'Pending')], default=2),
        ),
    ]
