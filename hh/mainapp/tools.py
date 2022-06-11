from mainapp.models import Users, CompanyProfile, UserProfile
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from loguru import logger


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
def get_user_data(request):
    user_data = {}
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user_item = Users.objects.get(id=user_id)
        except Exception as e:
            print(f'Ошибка поиска пользователя с id={user_id}. Возможно нарушение целостности данных!', e.args)
        else:
            if user_item.role_name_id == 2:
                user_profile_item = UserProfile.objects.get(user_name_id=user_id)
                company_profile_item = None
            elif user_item.role_name_id == 3:
                user_profile_item = None
                company_profile_item = CompanyProfile.objects.get(user_name_id=user_id)
            else:
                user_profile_item = None
                company_profile_item = None

            user_data = {'user': user_item,
                         'user_profile': user_profile_item,
                         'company_profile': company_profile_item}

    return user_data


@logger.catch
def is_applicant(func):
    """
    Декоратор проверяет:
     1. Авторизован ли пользователь?
     2. Авторизованный пользователь - соискатель?
    :param func:
    :return:
    """
    def wrap(request, *args, **kwargs):
        user_data = get_user_data(request)
        if user_data:
            if user_data['user'].role_name_id == 2:  # Соискатель?
                return func(request, *args, **kwargs)
            else:
                print('В лог: роль пользователя - не соискатель!')
                raise PermissionDenied
        else:
            print('В лог: не пройдена авторизация. Редирект на страницу авторизации')
            return HttpResponseRedirect(reverse('auth:login'))

    return wrap


@logger.catch
def is_employer(func):
    """
    Декоратор проверяет:
     1. Авторизован ли пользователь?
     2. Авторизованный пользователь - работодатель?
    :param func:
    :return:
    """
    def wrap(request, *args, **kwargs):
        user_data = get_user_data(request)
        try:
            user_item = user_data['user']
        except Exception as e:
            print('В лог: не пройдена авторизация. Редирект на страницу авторизации', e.args)
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            if user_item.role_name_id == 3:  # Работодатель?
                return func(request, *args, **kwargs)
            else:
                print('В лог: роль пользователя - не работодатель!')
                raise PermissionDenied

    return wrap
