import hashlib
import random
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.db import DatabaseError, transaction
from django.core.mail import send_mail
from django.conf import settings
from mainapp.models import Users, Roles, UserProfile, CompanyProfile
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
def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.login}'
    message = f'Для подтверждения учетной записи {user.login} на портале {settings.DOMAIN_NAME_VERBOSE} перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

@logger.catch
def check_user(username, password):
    try:
        user = Users.objects.get(login=username)
    except Exception as e:
        print(f'Error login user : {e.args}')
        return None
    else:
        if user.hash_password == hashlib.sha1((password + user.email).encode('utf8')).hexdigest():
            return user
        else:
            print('Wrong password!')
            return None

    return None

@logger.catch
def login(request):
    title = 'вход'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = check_user(username=username, password=password)
        if user:
            # request.session['user_item'] = user_item
            # if user_item.role_name_id == 2:
            #     try:
            #         user_profile_item = UserProfile.object.get(id=user_item.id)
            #     except Exception as e:
            #         print(f'Ошибка поиска профиля пользователя {user_item.login}:', e.args)
            #     else:
            #         request.session['user_profile_item'] = user_profile_item
            #
            # elif user_item.role_name_id == 3:
            #     try:
            #         company_profile_item = CompanyProfile.objects.get(id=user_item.id)
            #     except Exception as e:
            #         print(f'Ошибка поиска профиля компании {user_item.login}:', e.args)
            #     else:
            #         request.session['company_profile_item'] = company_profile_item

            request.session['user_id'] = user.id
            # request.session['user_name'] = user_item.login
            # request.session['role_id'] = user_item.role_name_id

            if user.role_name_id == 2:
                return HttpResponseRedirect(reverse('users:profile_main'))
            elif user.role_name_id == 3:
                # return HttpResponseRedirect(reverse('companies:company-profile'))
                return HttpResponseRedirect(reverse('companies:card_edit'))
            else:
                return HttpResponseRedirect(reverse('main'))
        else:
            return HttpResponseRedirect(reverse('auth:login'))

    content = {'title': title}

    return render(request, 'authapp/login.html', content)

@logger.catch
def logout(request):
    del request.session['user_id']
    # del request.session['user_name']
    # del request.session['role_id']

    return HttpResponseRedirect(reverse('main'))

@logger.catch
def register(request):
    title = 'Регистрация нового пользователя'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role_name = request.POST['rolename']
        role_object = Roles.objects.get(name=role_name)
        hash_password = hashlib.sha1((password + email).encode('utf8')).hexdigest()

        try:
            with transaction.atomic():
                user = Users(login=username,
                             hash_password=hash_password,
                             email=email,
                             role_name=role_object)
                user.save()

                user.is_active = False
                salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
                user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
                user.save()

                # Здесь пока чистый хардкод, исправлю
                if role_object.id == 2:
                    # Если роль пользователя - соискатель, добавляем строку в UserProfile
                    user_profile = UserProfile(
                        user_name_id=user.id,
                        last_name=username
                    )
                    user_profile.save()

                elif role_object.id == 3:
                    # Если роль пользователя - работодатель, добавляем строку в CompanyProfile
                    company_profile = CompanyProfile(
                        user_name_id=user.id,
                        name=username
                    )
                    company_profile.save()

                if send_verify_mail(user):
                    print('Сообщение для подтверждения учетной записи пользователя отправлено')
                    return HttpResponseRedirect(reverse('auth:login'))
                else:
                    print('Ошибка при отправке сообщения пользователю!')
                    return HttpResponseRedirect(reverse('auth:login'))

        except DatabaseError as e:
            print('Ошибка при сохранении данных!', e.args)

        return HttpResponseRedirect(reverse('auth:login'))

    roles_list = [item.name for item in Roles.objects.all() if item.id in [2, 3]]
    content = {'title': title,
               'username': '',
               'password': '',
               'email': '',
               'roles': roles_list}

    return render(request, 'authapp/register.html', content)

@logger.catch
def verify(request, email, activation_key):
    try:
        user = Users.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            return render(request, 'authapp/verify_confirm.html', {'title': 'Подтверждение регистрации', 'user': user})
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/login.html')
    except Exception as e:
        print(f'error activation user : {e.args}')

    return HttpResponseRedirect(reverse('main'))
