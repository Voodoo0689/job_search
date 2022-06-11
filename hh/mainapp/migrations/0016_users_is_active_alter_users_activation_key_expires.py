# Generated by Django 4.0.4 on 2022-05-10 12:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_users_activation_key_users_activation_key_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 12, 49, 52, 654669, tzinfo=utc)),
        ),
    ]
