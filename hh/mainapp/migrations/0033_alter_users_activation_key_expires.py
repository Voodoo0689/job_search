# Generated by Django 4.0.4 on 2022-05-27 12:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0032_alter_userprofile_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 12, 53, 46, 613635, tzinfo=utc)),
        ),
    ]