# Generated by Django 3.1 on 2020-09-04 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0008_auto_20200904_1123'),
        ('dashboard', '0012_auto_20200904_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proofofpayment',
            name='investment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.investmentplan'),
        ),
    ]