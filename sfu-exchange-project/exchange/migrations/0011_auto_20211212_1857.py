# Generated by Django 3.2.10 on 2021-12-12 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0010_questionvotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionvotes',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionvotes',
            name='user',
        ),
        migrations.AddField(
            model_name='question',
            name='voted',
            field=models.ManyToManyField(blank=True, default=None, related_name='vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionvotes',
            name='question_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='exchange.question'),
        ),
        migrations.AddField(
            model_name='questionvotes',
            name='user_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]