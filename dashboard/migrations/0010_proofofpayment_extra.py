# Generated by Django 3.1 on 2020-09-04 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20200904_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='proofofpayment',
            name='extra',
            field=models.TextField(blank=True, null=True),
        ),
    ]
