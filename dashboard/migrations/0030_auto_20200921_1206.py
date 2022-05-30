# Generated by Django 3.1 on 2020-09-21 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_auto_20200921_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referralpayment',
            name='referrer_reward',
        ),
        migrations.AddField(
            model_name='referralpayment',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='referralpayment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Paid'), (2, 'Unpaid'), (3, 'Pending')], default=2),
        ),
    ]