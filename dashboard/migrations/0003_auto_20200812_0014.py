# Generated by Django 3.1 on 2020-08-11 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_investmentplan'),
        ('dashboard', '0002_auto_20200811_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='investment_plan',
        ),
        migrations.AlterField(
            model_name='investment',
            name='investment_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.investmentplan'),
        ),
        migrations.AlterField(
            model_name='proofofpayment',
            name='investment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.investment'),
        ),
        migrations.DeleteModel(
            name='InvestmentPlan',
        ),
    ]
