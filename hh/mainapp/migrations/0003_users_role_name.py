# Generated by Django 4.0.4 on 2022-04-18 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_city_eduorg_users_birth_date_users_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='role_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.roles'),
        ),
    ]
