# Generated by Django 3.1 on 2020-09-11 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_notifications'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notifications',
            new_name='Notification',
        ),
    ]
