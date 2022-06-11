import hashlib
import json
import os
import random
from loguru import logger
from django.core.management.base import BaseCommand
from mainapp.models import City, Users, CompanyProfile, Vacancy, Articles, UserProfile
from mainapp.models import Categories, Roles, UserEdu, UserJobHistory, Resumes
from datetime import timedelta, datetime


JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for file_num in range(1, 10):
            resumes = load_from_json('resumes_file' + str(file_num))

            for key, value in resumes.items():
                if isinstance(value, list):
                    for user in value:
                        city_id = 0
                        try:
                            # search city
                            city = City.objects.get(name=user['location']['title'])
                        except Exception as e:
                            # try to append city if not found
                            try:
                                new_city = City()
                                new_city.name = user['location']['title']
                                new_city.save()
                            except Exception as e:
                                print(f'Ошибка при добавлении населенного пункта {user["location"]["title"]}: {e.args}')
                            else:
                                city_id = new_city.id
                        else:
                            city_id = city.id

                        user_id = 0
                        try:
                            # search user_item
                            user_item = Users.objects.get(login=user['id'])
                        except Exception as e:
                            # try to append user_item if not found
                            try:
                                new_user_item = Users()
                                new_user_item.login = user['id']
                                new_user_item.email = user['id'] + '@mail'
                                new_user_item.hash_password = hashlib.sha1(('111' + new_user_item.email).encode('utf8')).hexdigest()
                                new_user_item.avatar = user['avatar']['src']
                                new_user_item.role_name_id = 2
                                new_user_item.is_active = 1
                                new_user_item.comments = ''
                                new_user_item.save()
                            except Exception as e:
                                print(f'Ошибка при добавлении учетной записи пользователя {new_user_item.login}: {e.args}')
                            else:
                                try:
                                    # for new user append user profile
                                    user_profile = UserProfile()
                                    user_profile.user_name_id = new_user_item.id
                                    user_profile.last_name = user['title'].split(' ')[0]
                                    user_profile.first_name = user['title'].split(' ')[1]
                                    user_profile.middle_name = ''
                                    if user['age']['value']:
                                        user_profile.birth_date = datetime.now() - timedelta(days=365 * user['age']['value'])
                                    # user_profile.phone_num =
                                    user_profile.city_name_id = city_id
                                    user_profile.gender = 1
                                    user_profile.soft_skills = ', '.join(skill['title'] for skill in user['skills'])
                                    user_profile.comments = ''
                                    user_profile.save()
                                except Exception as e:
                                    print(f'Ошибка при добавлении профиля пользователя {user_profile.last_name}: {e.args}')

                                # append job history
                                try:
                                    user_job = UserJobHistory()
                                    user_job.user_name_id = new_user_item.id
                                    user_job.company_name = user['lastJob']['company']['title']
                                    user_job.start_date = datetime.now() - timedelta(days=30 * user['lastJob']['duration']['value'])
                                    user_job.position = user['lastJob']['position']
                                    user_job.save()
                                except Exception as e:
                                    print(f'Ошибка при добавлении последнего места работы {new_user_item.login}: {e.args}')

                                # append user educations
                                if user['education']:
                                    try:
                                        user_edu = UserEdu()
                                        user_edu.user_name_id = new_user_item.id
                                        user_edu.edu_org_name = user['education']['university']['title']
                                        user_edu.end_date = datetime.now()
                                        user_edu.edu_type = 1
                                        user_edu.course_name = user['education']['faculty']
                                        user_edu.skills = ''
                                        user_edu.save()
                                    except Exception as e:
                                        print(f'Ошибка при добавлении обучения {new_user_item.login}: {e.args}')

                                # append resume
                                try:
                                    user_resume = Resumes()
                                    user_resume.user_name_id = new_user_item.id
                                    if user['specialization']:
                                        user_resume.position_name = user['specialization'] + user['qualification']['title']
                                    if user['remoteWork']:
                                        user_resume.work_mode = 3
                                    else:
                                        user_resume.work_mode = 1
                                    if user['salary']:
                                        user_resume.min_salary =user['salary']['value']
                                    user_resume.publish_date = user['lastVisited']['date']
                                    user_resume.save()
                                except Exception as e:
                                    print(f'Ошибка при добавлении резюме {new_user_item.login}: {e.args}')
                        else:
                            # user exist!
                            pass
