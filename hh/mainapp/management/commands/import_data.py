import hashlib
import json
import os
import random
from loguru import logger
from django.core.management.base import BaseCommand
from mainapp.models import City, Users, CompanyProfile, Vacancy, Articles, UserProfile
from mainapp.models import Categories, Roles, UserEdu, UserJobHistory, Resumes

JSON_PATH = 'mainapp/json'


# логирование: настройки логера из библиотеки loguru
logger.add(
    "logs/debug.json",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 MB",
    compression="zip",
    serialize=True
)

@logger.catch
def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as infile:
        return json.load(infile)


@logger.catch
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Так как на удаление родительской записи наложен RESTRICT при наличии дочерних,
        # то очищаем таблицы снизу вверх
        Articles.objects.all().delete()
        UserJobHistory.objects.all().delete()
        Resumes.objects.all().delete()
        UserEdu.objects.all().delete()
        UserProfile.objects.all().delete()
        Vacancy.objects.all().delete()
        Categories.objects.all().delete()
        CompanyProfile.objects.all().delete()
        City.objects.all().delete()
        Users.objects.all().delete()
        Roles.objects.all().delete()

        for key, value in {'Администратор': 1,
                           'Соискатель': 2,
                           'Работодатель': 3,
                           'Модератор': 4}.items():
            new_role = Roles()
            new_role.id = value
            new_role.name = key
            new_role.save()

        default_role = Roles.objects.get(name='Работодатель')
        default_role_moderator = Roles.objects.get(name='Модератор')

        for item in ['Автомобильный бизнес',
                     'Административный персонал',
                     'Банки, инвестиции',
                     'Безопасность',
                     'Бухгалтерия, учет',
                     'Государственная служба',
                     'Информационные технологии',
                     'Искусство, развлечения',
                     'Маркетинг, реклама',
                     'Медицина, фармацевтика',
                     'Наука, образование',
                     'Продажи']:
            new_category = Categories()
            new_category.name = item
            new_category.save()

        default_category = Categories.objects.get(name='Информационные технологии')

        vacancies = load_from_json('vacancy')

        new_user_id = 0
        # try to append default user as a news moderator
        try:
            new_user_id += 1
            new_user = Users()
            new_user.id = new_user_id
            new_user.login = 'user0'
            new_user.email = new_user.login + '@mail'
            new_user.hash_password = hashlib.sha1(('zaq1@WSX' + new_user.email).encode('utf8')).hexdigest()
            new_user.role_name_id = default_role_moderator.id
            new_user.save()
        except Exception as e:
            print(f'Ошибка при добавлении учетной записи пользователя {new_user.login}: {e.args}')
        else:
            moderator = new_user

        for key, value in vacancies.items():
            city_id = 0
            try:
                # search city
                city = City.objects.get(name=value['city'])
            except Exception as e:
                # try to append city if not found
                try:
                    new_city = City()
                    new_city.name = value['city']
                    new_city.save()
                except Exception as e:
                    print(f'Ошибка при добавлении населенного пункта {value["city"]}: {e.args}')
                else:
                    city_id = new_city.id
            else:
                city_id = city.id

            try:
                # search company in CompanyProfile
                company = CompanyProfile.objects.get(name=value['employer_name'])
            except Exception as e:
                # try to append records in Users and CompanyProfile if not found
                new_user_id += 1
                company_id = new_user_id

                # try to append new user
                try:
                    new_user = Users()
                    new_user.id = new_user_id
                    new_user.login = 'user' + str(new_user_id)
                    new_user.email = new_user.login + '@mail'
                    new_user.hash_password = hashlib.sha1(('111' + new_user.email).encode('utf8')).hexdigest()
                    new_user.role_name_id = default_role.id
                    new_user.save()
                except Exception as e:
                    print(f'Ошибка при добавлении учетной записи пользователя {new_user.login}: {e.args}')
                else:
                    try:
                        # for new user append company profile
                        new_company = CompanyProfile()
                        new_company.user_name_id = new_user_id
                        new_company.name = value['employer_name']
                        new_company.city_name_id = city_id
                        new_company.save()
                    except Exception as e:
                        print(f'Ошибка при добавлении профиля компании {new_company.name}: {e.args}')

            else:
                company_id = company.user_name_id

            try:
                # for company profile append vacancy
                new_vacancy = Vacancy()
                new_vacancy.user_name_id = company_id
                new_vacancy.work_mode = random.randint(1, 5)
                new_vacancy.category_name_id = default_category.id
                new_vacancy.position_name = value['job_title']
                new_vacancy.city_name_id = city_id
                new_vacancy.requirements = value['job_desc']
                new_vacancy.conditions = value['job_requirement']
                new_vacancy.save()
            except Exception as e:
                print(f'Ошибка при добавлении профиля компании {new_vacancy.user_name_id}: {e.args}')

        articles = load_from_json('hh_news')
        for key, value in articles.items():
            try:
                new_article = Articles()
                new_article.id = key
                new_article.header = value['article_title']
                new_article.text = value['article_sub_title']
                new_article.url = value['article_url']
                new_article.user_name_id = moderator.id
                new_article.save()
            except Exception as e:
                print(f'Ошибка при добавлении новости id={key}: {e.args}')
