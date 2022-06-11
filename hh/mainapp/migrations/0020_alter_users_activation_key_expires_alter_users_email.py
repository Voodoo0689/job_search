# Generated by Django 4.0.4 on 2022-05-24 00:27

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_alter_useredu_edu_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 0, 27, 40, 511448, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=100, validators=[django.core.validators.EmailValidator], verbose_name='e-mail'),
        ),
    ]
