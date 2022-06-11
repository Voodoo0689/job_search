# Generated by Django 4.0.4 on 2022-04-27 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_vacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='min_salary',
            field=models.IntegerField(null=True, verbose_name='Минимальная ЗП'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='publish_date',
            field=models.DateField(null=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
    ]
