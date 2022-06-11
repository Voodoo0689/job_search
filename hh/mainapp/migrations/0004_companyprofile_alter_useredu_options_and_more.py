# Generated by Django 4.0.4 on 2022-04-20 12:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_users_role_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Наименование')),
                ('short_name', models.CharField(max_length=20, unique=True, verbose_name='Короткое наименование')),
                ('is_edu', models.BooleanField(verbose_name='Образовательное учреждение')),
                ('logo', models.ImageField(blank=True, upload_to='avatars')),
                ('comments', models.CharField(blank=True, max_length=100, verbose_name='Примечание')),
                ('city_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.city')),
            ],
            options={
                'verbose_name': 'Учебные заведения',
                'db_table': 'CompanyProfile',
            },
        ),
        migrations.AlterModelOptions(
            name='useredu',
            options={'verbose_name': 'Образование'},
        ),
        migrations.RemoveField(
            model_name='users',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='users',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='users',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='users',
            name='name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='phone_num',
        ),
        migrations.AddField(
            model_name='users',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars'),
        ),
        migrations.AddField(
            model_name='users',
            name='hash_password',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='users',
            name='login',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Логин'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, unique=True, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=50, unique=True, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=50, unique=True, verbose_name='Отчество')),
                ('birth_date', models.DateField(default=datetime.date(2022, 4, 20), verbose_name='Дата рождения')),
                ('phone_num', models.CharField(max_length=100, verbose_name='Телефоны')),
                ('home_address', models.CharField(blank=True, max_length=150, verbose_name='Домашний адрес')),
                ('gender', models.IntegerField(choices=[('Мужской', 1), ('Женский', 2)], default=1, verbose_name='Пол')),
                ('soft_skills', models.CharField(blank=True, max_length=100, verbose_name='soft skills')),
                ('hard_skills', models.CharField(blank=True, max_length=100, verbose_name='hard skills')),
                ('comments', models.CharField(blank=True, max_length=100, verbose_name='Примечание')),
                ('city_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.city')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.users')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'db_table': 'UserProfile',
            },
        ),
        migrations.CreateModel(
            name='UserJobHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала работы')),
                ('end_date', models.DateField(blank=True, verbose_name='Дата окончания работы')),
                ('position', models.CharField(blank=True, max_length=50, verbose_name='Должность')),
                ('progress', models.CharField(blank=True, max_length=200, verbose_name='Результат / достижения')),
                ('comments', models.CharField(blank=True, max_length=100, verbose_name='Примечание')),
                ('company_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.companyprofile')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.users')),
            ],
            options={
                'verbose_name': 'Трудовая деятельность',
                'db_table': 'UserJobHistory',
            },
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.users'),
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=100, verbose_name='Заголовок статьи')),
                ('text', models.TextField(blank=True, verbose_name='Содержание статьи')),
                ('publish_date', models.DateField(null=True, verbose_name='Дата публикации')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.users')),
            ],
            options={
                'verbose_name': 'Статьи',
                'db_table': 'Articles',
            },
        ),
        migrations.AlterField(
            model_name='useredu',
            name='edu_org_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.companyprofile'),
        ),
        migrations.DeleteModel(
            name='EduOrg',
        ),
    ]