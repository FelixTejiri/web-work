# Generated by Django 3.1 on 2020-09-04 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0005_sitesetting_teammember'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentplan',
            name='payment_date',
            field=models.DateField(null=True),
        ),
    ]
