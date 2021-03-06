# Generated by Django 3.2.10 on 2021-12-12 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0011_auto_20211212_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerVotes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='voted',
        ),
        migrations.AddField(
            model_name='answer',
            name='voted',
            field=models.ManyToManyField(blank=True, default=None, related_name='voted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='QuestionVotes',
        ),
        migrations.AddField(
            model_name='answervotes',
            name='answer_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='exchange.answer'),
        ),
        migrations.AddField(
            model_name='answervotes',
            name='user_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
