from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('partners_list/<int:page>/', mainapp.partners_list, name='partners_list'),
    path('articles_list/<int:page>/', mainapp.articles_list, name='articles_list'),
    path('vacancies_list/', mainapp.vacancies_list, name='vacancies_list'),
    path('vacancies_list/<int:page>', mainapp.vacancies_list, name='vacancies_list'),
    path('article_view/<int:article_id>/', mainapp.article_view, name='article_view'),
    path('article_edit/<int:article_id>/', mainapp.article_edit, name='article_edit'),
    path('vacancy_response/<int:vacancy_id>', mainapp.vacancy_response, name='vacancy_response'),
    path('partner_vacancies/<int:company_id>/', mainapp.partner_vacancies, name='partner_vacancies'),
    path('partner_reviews/<int:company_id>/', mainapp.partner_reviews, name='partner_reviews'),
    path('partner_news/<int:company_id>/', mainapp.partner_news, name='partner_news'),
    path('add_review/<int:company_id>/', mainapp.add_review, name='add_review'),
    path('send_message/<int:company_id>/', mainapp.send_message, name='send_message')
]