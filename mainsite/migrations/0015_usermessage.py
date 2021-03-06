# Generated by Django 3.1.2 on 2020-12-06 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0014_auto_20201206_0137'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(help_text='Subject of the message', max_length=50)),
                ('body', models.TextField(help_text='Body of the message')),
                ('should_publish', models.BooleanField(default=True)),
            ],
        ),
    ]
