# Generated by Django 4.0.4 on 2022-05-10 12:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_alter_articles_options_articles_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 12, 31, 31, 919703, tzinfo=utc)),
        ),
    ]