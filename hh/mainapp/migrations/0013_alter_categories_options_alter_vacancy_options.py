# Generated by Django 4.0.4 on 2022-05-02 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_categories_vacancy_category_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Категории вакансий', 'verbose_name_plural': 'Категории вакансий'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'Вакансии', 'verbose_name_plural': 'Вакансии'},
        ),
    ]
