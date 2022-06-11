from django.urls import path
import companyapp.views as companyapp

app_name = 'companyapp'

urlpatterns = [
    path('', companyapp.card_edit, name='card_edit'),
    path('card_edit/', companyapp.card_edit, name='card_edit'),
    path('vacancy_create/', companyapp.VacancyCreateView.as_view(), name='vacancy_create'),
    path('company_vacancies/', companyapp.VacancyListView.as_view(), name='company_vacancies'),
    path('vacancy_show/<int:pk>/', companyapp.VacancyDetailView.as_view(), name='vacancy_show'),
    path('vacancy_edit/<int:pk>/', companyapp.VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('vacancy_delete/<int:pk>/', companyapp.VacancyDeleteView.as_view(), name='vacancy_delete'),

    path('profile_security/', companyapp.profile_security, name='profile_security'),
    path('reviews/', companyapp.ReviewListView.as_view(), name='reviews'),
    path('review_show/<int:pk>/', companyapp.ReviewDetailView.as_view(), name='review_show'),

    path('news_create/', companyapp.NewsCreateView.as_view(), name='news_create'),
    path('news/', companyapp.NewsListView.as_view(), name='news'),
    path('news_show/<int:pk>/', companyapp.NewsDetailView.as_view(), name='news_show'),
    path('news_edit/<int:pk>/', companyapp.NewsUpdateView.as_view(), name='news_edit'),
    path('news_delete/<int:pk>/', companyapp.NewsDeleteView.as_view(), name='news_delete'),
    path('message_list/', companyapp.message_list, name='message_list'),
    path('view_message/<int:message_id>/', companyapp.view_message, name='view_message'),
    path('reply_message/<int:message_id>/', companyapp.reply_message, name='reply_message'),
]
