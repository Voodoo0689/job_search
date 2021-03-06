# Generated by Django 4.0.4 on 2022-05-24 01:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_alter_userprofile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.city', validators=[mainapp.models.check_rus_letters_only]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=50, validators=[mainapp.models.check_rus_letters_only], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=50, validators=[mainapp.models.check_rus_letters_only], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='middle_name',
            field=models.CharField(max_length=50, validators=[mainapp.models.check_rus_letters_only], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 1, 32, 42, 903024, tzinfo=utc)),
        ),
    ]
