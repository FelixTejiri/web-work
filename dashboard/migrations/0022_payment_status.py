# Generated by Django 3.1 on 2020-09-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_investment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]