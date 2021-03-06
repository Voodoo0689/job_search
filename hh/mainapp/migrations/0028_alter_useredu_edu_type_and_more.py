# Generated by Django 4.0.4 on 2022-05-25 05:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0027_alter_users_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useredu',
            name='edu_type',
            field=models.IntegerField(choices=[(1, 'Высшее образование'), (2, 'Среднее специальное образование'), (3, 'Повышение квалификации / Переквалификация')], default=1, validators=[mainapp.models.check_edu_choices], verbose_name='Уровень образования'),
        ),
        migrations.AlterField(
            model_name='users',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 27, 5, 50, 30, 223899, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Resumes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=50, verbose_name='Должность')),
                ('work_mode', models.IntegerField(choices=[(1, 'Полный рабочий день'), (2, 'Частичная занятость'), (3, 'Удаленное место работы'), (4, 'Вахтовый метод работы'), (5, 'Проектная работа')], default=1, verbose_name='Тип занятости')),
                ('min_salary', models.IntegerField(null=True, verbose_name='Минимальная ЗП')),
                ('publish_date', models.DateField(null=True, verbose_name='Дата публикации')),
                ('comments', models.CharField(blank=True, max_length=100, verbose_name='Примечание')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.users')),
            ],
            options={
                'verbose_name': 'Резюме соискателей',
                'verbose_name_plural': 'Резюме соискателей',
                'db_table': 'Resumes',
            },
        ),
    ]
