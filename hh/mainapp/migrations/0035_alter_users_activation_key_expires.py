# Generated by Django 4.0.4 on 2022-05-31 02:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0034_alter_companyprofile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 2, 42, 7, 104839, tzinfo=utc)),
        ),
    ]