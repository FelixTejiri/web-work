# Generated by Django 3.1 on 2020-09-18 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_auto_20200911_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.user')),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='my_refferals', to='dashboard.user')),
            ],
        ),
        migrations.CreateModel(
            name='ReferralPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referrer_reward', models.FloatField(null=True)),
                ('referral', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.referral')),
            ],
        ),
    ]
