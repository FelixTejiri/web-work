# Generated by Django 3.1 on 2020-08-25 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20200823_1654'),
        ('mainsite', '0003_investmentplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('is_account_valid', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.user')),
            ],
        ),
    ]