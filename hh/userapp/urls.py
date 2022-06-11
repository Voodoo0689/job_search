from django.urls import path
import userapp.views as userapp

app_name = 'userapp'

urlpatterns = [
    path('', userapp.profile_main, name='profile_main'),
    path('profile_contacts/', userapp.profile_contacts, name='profile_contacts'),
    path('profile_edu/', userapp.profile_edu, name='profile_edu'),
    path('edu_append/', userapp.edu_append, name='edu_append'),
    path('edu_update/<int:item_id>', userapp.edu_update, name='edu_update'),
    path('edu_delete/<int:item_id>', userapp.edu_delete, name='edu_delete'),
    path('profile_job/', userapp.profile_job, name='profile_job'),
    path('job_append/', userapp.job_append, name='job_append'),
    path('job_update/<int:item_id>', userapp.job_update, name='job_update'),
    path('job_delete/<int:item_id>', userapp.job_delete, name='job_delete'),
    path('profile_security/', userapp.profile_security, name='profile_security'),
    path('profile_resume/', userapp.profile_resume, name='profile_resume'),
    path('resume_append/', userapp.resume_append, name='resume_append'),
    path('resume_update/<int:item_id>', userapp.resume_update, name='resume_update'),
    path('resume_delete/<int:item_id>', userapp.resume_delete, name='resume_delete'),
    path('resume_export/<int:item_id>', userapp.resume_export, name='resume_export'),
    path('resume_view/<int:item_id>', userapp.resume_view, name='resume_view'),
    path('message_list/', userapp.message_list, name='message_list'),
    path('view_message/<int:message_id>', userapp.view_message, name='view_message'),
    path('reply_message/<int:message_id>', userapp.reply_message, name='reply_message'),
]