# Generated by Django 3.2.10 on 2021-12-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0010_notification_notification_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(default='post', max_length=256),
        ),
    ]
