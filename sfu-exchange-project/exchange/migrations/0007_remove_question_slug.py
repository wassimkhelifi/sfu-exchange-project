# Generated by Django 3.2.9 on 2021-11-27 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_question_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='slug',
        ),
    ]
