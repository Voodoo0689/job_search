from django.db import connection
from django.shortcuts import render, HttpResponseRedirect
from django.db import DatabaseError
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import Articles, CompanyProfile, Vacancy, Roles, City, Users, Resumes, Review, News, Message
from django.conf import settings
from django.core.mail import send_mail
from mainapp.tools import get_user_data, is_applicant
from mainapp.forms import ReviewForm, MessageForm
from loguru import logger
import datetime
from statistics import mean
from rest_framework.viewsets import ModelViewSet
from mainapp.serializer import *
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


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
def get_page_num_list(page_num, max_page):
    page_set = set()
    sorted_page_list = []
    res_list = []

    if max_page <= 7:
        page_set = (i for i in range(1, max_page + 1))
    else:
        page_set.add(1)
        page_set.add(2)
        if page_num in range(2, max_page):
            page_set.add(page_num-1)
            page_set.add(page_num)
            page_set.add(page_num+1)
        page_set.add(max_page-1)
        page_set.add(max_page)

    sorted_page_list = sorted(list(page_set))
    for i in range(len(sorted_page_list)-1):
        if sorted_page_list[i+1] - sorted_page_list[i] == 1:
            res_list.append(sorted_page_list[i])
        else:
            res_list.append(sorted_page_list[i])
            res_list.append('...')
    res_list.append(sorted_page_list[-1])

    return res_list


@logger.catch
def main(request):
    title = 'Главная'
    # Добавим в контекст последние 5 новостей
    articles = Articles.objects.all()[:5]

    # Добавим в контекст список из 10 компаний с самым большим количеством вакансий
    with connection.cursor() as cursor:
        cursor.execute("SELECT b.name, count(a.id) as vacancy_count "
                       "FROM vacancy a, companyprofile b "
                       "WHERE a.user_name_id = b.user_name_id "
                       "GROUP BY a.user_name_id "
                       "ORDER BY vacancy_count DESC "
                       "LIMIT 10")
        top_companies = cursor.fetchall()

    user_data = get_user_data(request)
    content = {'title': title,
               'articles': articles,
               'top_companies': top_companies,
               **user_data}

    return render(request, 'mainapp/index.html', content)


@logger.catch
def partners_list(request, page=1):
    title = 'Компании-партнеры'

    user_data = get_user_data(request)

    with connection.cursor() as cursor:
        cursor.execute("SELECT b.user_name_id, b.name, count(a.id) as vacancy_count "
                       "FROM vacancy a, companyprofile b "
                       "WHERE a.user_name_id = b.user_name_id "
                       "GROUP BY a.user_name_id "
                       "ORDER BY vacancy_count DESC ")
        partners = cursor.fetchall()

    paginator = Paginator(partners, 10)
    # get page numbers as list
    page_list = get_page_num_list(page, paginator.num_pages)
    try:
        company_paginator = paginator.page(page)
    except PageNotAnInteger:
        company_paginator = paginator.page(1)
    except EmptyPage:
        company_paginator = paginator.page(paginator.num_pages)

    partners_lst = []
    for company in company_paginator:
        rates = [review.rate for review in Review.objects.filter(user_to_id=company[0])]
        avg_rate = 0
        if rates:
            avg_rate = round(mean(rates))

        partners_lst.append({'company_id': company[0],
                             'company_name': company[1],
                             'vacancy_count': company[2],
                             'company_rate': avg_rate,
                             'company': CompanyProfile.objects.get(user_name_id=company[0])})

    content = {'title': title,
               'page_list': page_list,
               'company_paginator': company_paginator,
               'partners': partners_lst,
               'rates': range(1, 6),
               **user_data}

    return render(request, 'mainapp/partners.html', content)


@logger.catch
def articles_list(request, page=1):
    title = 'Новости портала'

    user_data = get_user_data(request)

    paginator = Paginator(Articles.objects.all().order_by('-publish_date'), 5)
    # get page numbers as a list
    page_list = get_page_num_list(page, paginator.num_pages)
    try:
        articles_paginator = paginator.page(page)
    except PageNotAnInteger:
        articles_paginator = paginator.page(1)
    except EmptyPage:
        articles_paginator = paginator.page(paginator.num_pages)

    content = {'title': title,
               'page_list': page_list,
               'articles': articles_paginator,
               **user_data}

    return render(request, 'mainapp/articles.html', content)


@logger.catch
def article_view(request, article_id):
    title = 'Просмотр статьи'
    user_data = get_user_data(request)
    article = Articles.objects.get(id=article_id)

    content = {'title': title,
               'article': article,
               'prev_page': request.META.get('HTTP_REFERER'),
               **user_data}

    return render(request, 'mainapp/article_view.html', content)


@logger.catch
def article_edit(request, article_id):
    title = 'Редактирование статьи'

    article = Articles.objects.get(id=article_id)

    if request.method == 'POST':
        try:
            article.header = request.POST['header']
            article.text = request.POST['text']
            article.url = request.POST['url']
            article.user_name_id = request.session.get('user_id')
            article.publish_date = datetime.date.today()
            article.save()
        except DatabaseError as e:
            print(f'Ошибка при сохранении статьи в базу данных: {e.args}')
        else:
            return HttpResponseRedirect(reverse('articles:article_view', args=[article_id,]))

    # TODO: need to check role_id
    # cancel editing article if role_id is not equal 4
    role_id = request.session.get('role_id')
    if role_id != 4:
        return HttpResponseRedirect(reverse(request.META.get('HTTP_REFERER')))
    else:
        user_data = get_user_data(request)
        content = {'title': title,
                   'article': article,
                   'prev_page': request.META.get('HTTP_REFERER'),
                   **user_data}

    return render(request, 'mainapp/article_edit.html', content)


@logger.catch
def vacancies_list(request, page=1):
    title = 'Вакансии'

    user_data = get_user_data(request)
    company_id, city_id, wm1, wm2, wm3, wm4, wm5 = 0, 0, 0, 0, 0, 0, 0
    skills = ''

    if request.method == 'POST':
        # get params from request
        company_id = int(request.POST.get('company_id', 0))
        city_id = int(request.POST.get('city_id', 0))
        skills = request.POST.get('skills', '')
        wm1 = request.POST.get('wm1', 0)
        wm2 = request.POST.get('wm2', 0)
        wm3 = request.POST.get('wm3', 0)
        wm4 = request.POST.get('wm4', 0)
        wm5 = request.POST.get('wm5', 0)
    elif request.method == 'GET':
        # get params from request
        # Здесь намеренно используем int, так как через request.GET все параметры - строковые
        page = int(request.GET.get('page', 0))
        company_id = int(request.GET.get('company_id', 0))
        city_id = int(request.GET.get('city_id', 0))
        skills = request.GET.get('skills', '')
        wm1 = int(request.GET.get('wm1', 0))
        wm2 = int(request.GET.get('wm2', 0))
        wm3 = int(request.GET.get('wm3', 0))
        wm4 = int(request.GET.get('wm4', 0))
        wm5 = int(request.GET.get('wm5', 0))

    work_mode_list = [item for item in [wm1, wm2, wm3, wm4, wm5] if item]

    # Сортировку можно сделать по publish_date, но это поле в тестовых данных не заполнено
    # Применяем цепочку фильтров
    vacancies = Vacancy.objects.all().order_by('id')
    if company_id:
        vacancies = vacancies.filter(user_name_id=company_id)
    if city_id:
        vacancies = vacancies.filter(city_name_id=city_id)
    if skills:
        vacancies = vacancies.filter(position_name__contains=skills)
    if work_mode_list:
        vacancies = vacancies.filter(work_mode__in=work_mode_list)
    paginator = Paginator(vacancies, 10)

    page_list = get_page_num_list(page, paginator.num_pages)
    try:
        vacancies_paginator = paginator.page(page)
    except PageNotAnInteger:
        vacancies_paginator = paginator.page(1)
    except EmptyPage:
        # vacancies_paginator = paginator.page(paginator.num_pages)
        vacancies_paginator = paginator.page(1)

    for vacancy in vacancies_paginator:
        vacancy.employer_name = CompanyProfile.objects.get(user_name_id=vacancy.user_name_id).name
        vacancy.work_mode = dict(Vacancy.WORK_MODE)[vacancy.work_mode]

    companies = CompanyProfile.objects.all().order_by('name')
    cities = City.objects.all().order_by('name')

    content = {'title': title,
               'page_list': page_list,
               'vacancies': vacancies_paginator,
               'companies': companies,
               'cities': cities,
               'company_id': company_id,
               'city_id': city_id,
               'skills': skills,
               'wm1': wm1,
               'wm2': wm2,
               'wm3': wm3,
               'wm4': wm4,
               'wm5': wm5,
               **user_data}

    return render(request, 'mainapp/vacancies.html', content)


def about(request):
    title = 'О проекте HH GB'

    user_data = get_user_data(request)
    content = {'title': title,
               **user_data}

    return render(request, 'mainapp/about.html', content)


@logger.catch
@is_applicant
def vacancy_response(request, vacancy_id):

    vacancy_item = Vacancy.objects.get(id=vacancy_id)
    company_item = Users.objects.get(id=vacancy_item.user_name_id)
    company_profile_item = CompanyProfile.objects.get(user_name_id=vacancy_item.user_name_id)

    user_data = get_user_data(request)
    applicant_item = user_data['user'].id
    try:
        resume_item = Resumes.objects.get(user_name_id=user_data['user_id'])
    except Exception as e:
        print('Возникло исключение при поиске резюме пользователя', e.args)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        resume_link = reverse('users:resume_view', args=[resume_item.id])

        # send email to company
        title = f'Отклик на вакансию {vacancy_item.position_name}'
        message = f'Вам направлен на рассмотрение отклик на вакансию. Резюме соискателя можно просмотреть по ссылке: {settings.DOMAIN_NAME}{resume_link}'
        send_to_company = send_mail(title, message, settings.EMAIL_HOST_USER, [company_item.email], fail_silently=False)

        # send email to applicant
        title = f'Отклик на вакансию {vacancy_item.position_name}'
        message = f'Ваше резюме отправлено на рассмотрение в {company_profile_item.name}'
        send_to_applicant = send_mail(title, message, settings.EMAIL_HOST_USER, [applicant_item.email], fail_silently=False)

        content = {'title': 'Отклик на вакансию',
                   'vacancy_item': vacancy_item,
                   'company_item': company_item,
                   'applicant_item': applicant_item,
                   'send_to_company': send_to_company,
                   'send_to_applicant': send_to_applicant}

        return render(request, 'mainapp/vacancy_response.html', content)


@logger.catch
def partner_vacancies(request, company_id):

    title = 'Вакансии ' + CompanyProfile.objects.get(user_name_id=company_id).name

    user_data = get_user_data(request)
    vacancies = Vacancy.objects.filter(user_name_id=company_id)

    for vacancy in vacancies:
        vacancy.work_mode = dict(Vacancy.WORK_MODE)[vacancy.work_mode]

    content = {'title': title,
               'vacancies': vacancies,
               **user_data}

    return render(request, 'mainapp/partner_vacancies.html', content)


@logger.catch
def partner_reviews(request, company_id):

    title = 'Отзывы о ' + CompanyProfile.objects.get(user_name_id=company_id).name

    user_data = get_user_data(request)
    reviews = Review.objects.filter(user_to_id=company_id)

    content = {'title': title,
               'reviews': reviews,
               'company_id': company_id,
               'rates': range(1, 6),
               **user_data}

    return render(request, 'mainapp/partner_reviews.html', content)


@logger.catch
def add_review(request, company_id):
    title = 'Добавить отзыв о ' + CompanyProfile.objects.get(user_name_id=company_id).name
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                review = Review()
                review.user_from_id = user_data['user'].id
                review.user_to_id = company_id
                review.content = request.POST['content']
                review.rate = request.POST['rate']
                review.save()
            except DatabaseError as e:
                print(f'Ошибка при сохранении отзыва в базу данных: {e.args}')
            else:
                return HttpResponseRedirect(reverse('partners:partner_reviews', args=[company_id, ]))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = ReviewForm()

    content = {'title': title,
               'form': form,
               'company_id': company_id,
               **user_data}

    return render(request, 'mainapp/review_edit.html', content)


@logger.catch
def partner_news(request, company_id):

    title = 'Новости ' + CompanyProfile.objects.get(user_name_id=company_id).name

    user_data = get_user_data(request)
    news = News.objects.filter(user_name_id=company_id)

    content = {'title': title,
               'news': news,
               'company_id': company_id,
               **user_data}

    return render(request, 'mainapp/partner_news.html', content)


@logger.catch
@is_applicant
def send_message(request, company_id):
    title = 'Отправить сообщение ' + CompanyProfile.objects.get(user_name_id=company_id).name
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                message = Message()
                message.from_user_name_id = user_data['user'].id
                message.to_user_name_id = company_id
                message.text = request.POST['text']
                message.save()
            except DatabaseError as e:
                print(f'Ошибка при сохранении сообщения в базу данных: {e.args}')
            else:
                return HttpResponseRedirect(request.POST['prev_page'])
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = MessageForm()

    content = {'title': title,
               'form': form,
               'company_id': company_id,
               'prev_page': request.META.get('HTTP_REFERER'),
               **user_data}

    return render(request, 'mainapp/send_message.html', content)


class UserModelViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersModelSerializer


class CityModelViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityModelSerializer


class UserProfileModelViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer


class RolesModelViewSet(ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesModelSerializer


class CompanyProfileModelViewSet(ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileModelSerializer


class UserEduModelViewSet(ModelViewSet):
    queryset = UserEdu.objects.all()
    serializer_class = UserEduModelSerializer


class UserJobHistoryModelViewSet(ModelViewSet):
    queryset = UserJobHistory.objects.all()
    serializer_class = UserJobHistoryModelSerializer


class ArticlesModelViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesModelSerializer


class CategoriesModelViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesModelSerializer


class VacancyModelViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyModelSerializer


class ResumesModelViewSet(ModelViewSet):
    queryset = Resumes.objects.all()
    serializer_class = ResumesModelSerializer
