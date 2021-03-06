# Generated by Django 4.0.4 on 2022-05-24 06:47

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_alter_userprofile_city_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useredu',
            name='comments',
            field=models.CharField(blank=True, max_length=100, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.city'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_num',
            field=models.CharField(max_length=100, validators=[mainapp.models.check_digits_only], verbose_name='Телефоны'),
        ),
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 6, 47, 37, 759433, tzinfo=utc)),
        ),
    ]
