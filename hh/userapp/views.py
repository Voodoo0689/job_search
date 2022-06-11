import hashlib
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.db import DatabaseError
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.urls import reverse
from mainapp.models import Users, Roles, UserProfile, City, UserEdu, UserJobHistory, Resumes, Message
from authapp.views import check_user
from .forms import UserEduForm, UserJobHistoryForm, ResumeForm, UserContactsForm, UserMainForm, MessageForm
from .export_resume import export_resume
from mainapp.tools import get_user_data, is_applicant
from loguru import logger
from django.db.models import Q


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
@is_applicant
def profile_main(request):
    title = 'Личный кабинет соискателя'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = UserMainForm(request.POST)
        if form.is_valid():
            user_profile = user_data['user_profile']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.middle_name = form.cleaned_data['middle_name']
            user_profile.birth_date = form.cleaned_data['birth_date']
            user_profile.phone_num = form.cleaned_data['phone_num']
            user_profile.gender = form.cleaned_data['gender']
            user_profile.soft_skills = form.cleaned_data['soft_skills']
            user_profile.hard_skills = form.cleaned_data['hard_skills']
            user_profile.comments = form.cleaned_data['comments']
            user_profile.save()
            return HttpResponseRedirect(reverse('users:profile_main'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = UserMainForm(instance=user_data['user_profile'])

    content = {'title': title,
               'form': form,
               **user_data}

    return render(request, 'userapp/profile-main.html', content)


@logger.catch
@is_applicant
def profile_contacts(request):
    title = 'Личный кабинет соискателя'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = UserContactsForm(request.POST)
        if form.is_valid():
            user = user_data['user']
            if request.FILES:
                user.avatar = request.FILES['file_photo']
            user.email = form.cleaned_data['email']
            user.comments = form.cleaned_data['comments']
            user.save()
            return HttpResponseRedirect(reverse('users:profile_contacts'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = UserContactsForm(instance=user_data['user'])

    content = {'title': title,
               'form': form,
               **user_data}

    return render(request, 'userapp/profile-contacts.html', content)


@logger.catch
@is_applicant
def profile_edu(request):
    title = 'Образование'

    user_data = get_user_data(request)
    user = user_data['user']
    user_edu = UserEdu.objects.all().filter(user_name_id=user.id)
    for item in user_edu:
        item.edu_type = dict(UserEdu.EDU_CHOICES)[item.edu_type]

    content = {'title': title,
               'user_edu': user_edu,
               **user_data}

    return render(request, 'userapp/profile-edu.html', content)


@logger.catch
@is_applicant
def edu_append(request):
    title = 'Добавить строку об образовании'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = UserEduForm(request.POST)
        if form.is_valid():
            user_edu_item = UserEdu()
            user_edu_item.user_name_id = user_data['user'].id
            user_edu_item.edu_org_name = form.cleaned_data['edu_org_name']
            user_edu_item.end_date = form.cleaned_data['end_date']
            user_edu_item.edu_type = form.cleaned_data['edu_type']
            user_edu_item.course_name = form.cleaned_data['course_name']
            user_edu_item.skills = form.cleaned_data['skills']
            if request.FILES:
                user_edu_item.photo = request.FILES['file_photo']
            user_edu_item.comments = form.cleaned_data['comments']
            user_edu_item.save()
            return HttpResponseRedirect(reverse('users:profile_edu'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = UserEduForm()

    content = {'title': title,
               'url': '/user_profile/edu_append/',
               'form': form,
               **user_data}

    return render(request, 'userapp/edu-update.html', content)


@logger.catch
@is_applicant
def edu_update(request, item_id):
    title = 'Редактировать строку об образовании'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = UserEduForm(request.POST, request.FILES)
        if form.is_valid():
            user_edu_item = UserEdu.objects.get(id=item_id)
            user_edu_item.user_name_id = user_data['user'].id
            user_edu_item.edu_org_name = form.cleaned_data['edu_org_name']
            user_edu_item.end_date = form.cleaned_data['end_date']
            user_edu_item.edu_type = form.cleaned_data['edu_type']
            user_edu_item.course_name = form.cleaned_data['course_name']
            user_edu_item.skills = form.cleaned_data['skills']
            if request.FILES:
                user_edu_item.photo = request.FILES['file_photo']
            user_edu_item.comments = form.cleaned_data['comments']
            user_edu_item.save()
            return HttpResponseRedirect(reverse('users:profile_edu'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        user_edu_item = UserEdu.objects.get(id=item_id)
        form = UserEduForm(instance=user_edu_item)
        print('PHOTO', form['photo'])

    content = {'title': title,
               'url': '/user_profile/edu_update/'+str(item_id),
               'form': form,
               'doc_photo': user_edu_item.photo,
               **user_data}

    return render(request, 'userapp/edu-update.html', content)


@logger.catch
@is_applicant
def edu_delete(request, item_id):

    if item_id:
        user_edu_item = UserEdu.objects.get(id=item_id)
        user_edu_item.delete()

    return HttpResponseRedirect(reverse('users:profile_edu'))


@logger.catch
@is_applicant
def profile_job(request):
    title = 'Трудовая деятельность'
    user_data = get_user_data(request)
    user_job = UserJobHistory.objects.all().filter(user_name_id=user_data['user'].id)
    content = {'title': title,
               'user_job': user_job,
               **user_data}

    return render(request, 'userapp/profile-job.html', content)


@logger.catch
@is_applicant
def job_append(request):
    title = 'Добавить период трудовой деятельности'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = UserJobHistoryForm(request.POST)
        if form.is_valid():
            user_job_item = UserJobHistory()
            user_job_item.user_name_id = user_data['user'].id
            user_job_item.company_name = form.cleaned_data['company_name']
            user_job_item.start_date = form.cleaned_data['start_date']
            if request.POST['end_date'] == '':
                user_job_item.end_date = None
            else:
                user_job_item.end_date = form.cleaned_data['end_date']
            user_job_item.position = form.cleaned_data['position']
            user_job_item.progress = form.cleaned_data['progress']
            user_job_item.comments = form.cleaned_data['comments']
            user_job_item.save()

            return HttpResponseRedirect(reverse('users:profile_job'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = UserJobHistoryForm()

    content = {'title': title,
               'url': '/user_profile/job_append/',
               'form': form,
               **user_data}

    return render(request, 'userapp/job-update.html', content)


@logger.catch
@is_applicant
def job_update(request, item_id):
    title = 'Редактировать строку о трудовой деятельности'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = UserJobHistoryForm(request.POST)
        if form.is_valid():
            user_job_item = UserJobHistory.objects.get(id=item_id)
            user_job_item.user_name_id = user_data['user'].id
            user_job_item.company_name = form.cleaned_data['company_name']
            user_job_item.start_date = form.cleaned_data['start_date']
            if request.POST['end_date'] == '':
                user_job_item.end_date = None
            else:
                user_job_item.end_date = form.cleaned_data['end_date']
            user_job_item.position = form.cleaned_data['position']
            user_job_item.progress = form.cleaned_data['progress']
            user_job_item.comments = form.cleaned_data['comments']
            user_job_item.save()
            return HttpResponseRedirect(reverse('users:profile_job'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        user_job_item = UserJobHistory.objects.get(id=item_id)
        form = UserJobHistoryForm(instance=user_job_item)

    content = {'title': title,
               'url': '/user_profile/job_update/'+str(item_id),
               'form': form,
               **user_data}

    return render(request, 'userapp/job-update.html', content)


@logger.catch
@is_applicant
def job_delete(request, item_id):

    if item_id:
        user_job_item = UserJobHistory.objects.get(id=item_id)
        user_job_item.delete()

    return HttpResponseRedirect(reverse('users:profile_job'))


@logger.catch
@is_applicant
def profile_security(request):
    title = 'Безопасность'
    user_data = get_user_data(request)

    if request.method == 'POST':
        user = user_data['user']
        if request.POST['prev_password']:
            if check_user(user.login, request.POST['prev_password']):
                if request.POST['new_password']:
                    user.hash_password = hashlib.sha1((request.POST['new_password'] +
                                                       user.email).encode('utf8')).hexdigest()
            else:
                return HttpResponse('Введенный старый пароль не правильный!')

        user.save()

    content = {'title': title,
               **user_data}

    return render(request, 'userapp/profile-security.html', content)


@logger.catch
@is_applicant
def profile_resume(request):
    title = 'Мои резюме'
    user_data = get_user_data(request)
    user_resume = Resumes.objects.all().filter(user_name_id=user_data['user'].id)
    for item in user_resume:
        item.work_mode = dict(Resumes.WORK_MODE)[item.work_mode]

    content = {'title': title,
               'resumes': user_resume,
               **user_data}

    return render(request, 'userapp/profile-resume.html', content)


@logger.catch
@is_applicant
def resume_append(request):
    title = 'Создать новое резюме'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume_item = Resumes()
            resume_item.user_name_id = user_data['user'].id
            resume_item.position_name = form.cleaned_data['position_name']
            resume_item.min_salary = form.cleaned_data['min_salary']
            resume_item.work_mode = form.cleaned_data['work_mode']
            resume_item.comments = form.cleaned_data['comments']
            resume_item.save()

            return HttpResponseRedirect(reverse('users:profile_resume'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = ResumeForm()

    content = {'title': title,
               'url': '/user_profile/resume_append/',
               'form': form,
               **user_data}

    return render(request, 'userapp/resume-update.html', content)


@logger.catch
@is_applicant
def resume_update(request, item_id):
    title = 'Редактировать резюме'
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume_item = Resumes.objects.get(id=item_id)
            resume_item.user_name_id = user_data['user'].id
            resume_item.position_name = form.cleaned_data['position_name']
            resume_item.min_salary = form.cleaned_data['min_salary']
            resume_item.work_mode = form.cleaned_data['work_mode']
            resume_item.comments = form.cleaned_data['comments']
            resume_item.save()
            return HttpResponseRedirect(reverse('users:profile_resume'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        resume_item = Resumes.objects.get(id=item_id)
        form = ResumeForm(instance=resume_item)

    content = {'title': title,
               'url': '/user_profile/resume_update/'+str(item_id),
               'form': form,
               **user_data}

    return render(request, 'userapp/resume-update.html', content)


@logger.catch
@is_applicant
def resume_delete(request, item_id):

    if item_id:
        resume_item = Resumes.objects.get(id=item_id)
        resume_item.delete()

    return HttpResponseRedirect(reverse('users:profile_resume'))


@logger.catch
@is_applicant
def resume_export(request, item_id):

    user_data = get_user_data(request)

    if item_id:
        resume_item = Resumes.objects.get(id=item_id)
        resume_item.work_mode = Resumes.WORK_MODE_DICT[resume_item.work_mode]
        user = user_data['user']
        user_profile = user_data['user_profile']
        user_profile.gender = UserProfile.GENDER_DICT[user_profile.gender]
        user_edu_history = UserEdu.objects.filter(user_name_id=user.id).order_by('-end_date')
        for item in user_edu_history:
            item.edu_type = UserEdu.EDU_DICT[item.edu_type]
        user_job_history = UserJobHistory.objects.filter(user_name_id=user.id).order_by('-start_date')
        export_resume(user=user,
                      user_profile=user_profile,
                      user_resume=resume_item,
                      user_edu_history=user_edu_history,
                      user_job_history=user_job_history)

    return HttpResponseRedirect(reverse('users:profile_resume'))


@logger.catch
@is_applicant
def resume_view(request, item_id):
    title = 'Просмотр резюме'
    user_data = get_user_data(request)

    resume_item = Resumes.objects.get(id=item_id)
    resume_item.work_mode = Resumes.WORK_MODE_DICT[resume_item.work_mode]
    user_item = user_data['user']
    user_profile_item = user_data['user_profile']
    user_profile_item.gender = UserProfile.GENDER_DICT[user_profile_item.gender]
    user_job_history = UserJobHistory.objects.filter(user_name_id=user_item.id).order_by('-start_date')
    user_edu_history = UserEdu.objects.filter(user_name_id=user_item.id).order_by('-end_date')
    for item in user_edu_history:
        item.edu_type = UserEdu.EDU_DICT[item.edu_type]

    content = {'title': title,
               'user': user_item,
               'user_profile_item': user_profile_item,
               'resume_item': resume_item,
               'user_job_history': user_job_history,
               'user_edu_history': user_edu_history
               }

    return render(request, 'userapp/resume-view.html', content)


@logger.catch
@is_applicant
def message_list(request):
    title = 'Сообщения'

    user_data = get_user_data(request)
    messages = Message.objects.filter(Q(from_user_name_id=user_data['user'].id) | Q(to_user_name_id=user_data['user'].id)).order_by('-send_date')

    content = {'title': title,
               'messages': messages,
               **user_data}

    return render(request, 'userapp/messages.html', content)


@logger.catch
@is_applicant
def view_message(request, message_id):
    title = 'Просмотр сообщения # ' + str(message_id)

    user_data = get_user_data(request)

    content = {'title': title,
               'message': Message.objects.get(id=message_id),
               **user_data}

    return render(request, 'userapp/view_message.html', content)


@logger.catch
@is_applicant
def reply_message(request, message_id):
    title = 'Ответить на сообщение ' + str(message_id)
    orig_message = Message.objects.get(id=message_id)
    user_data = get_user_data(request)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                message = Message()
                message.reply_to_message_id = message_id
                message.from_user_name_id = user_data['user'].id
                message.to_user_name_id = orig_message.from_user_name_id
                message.text = request.POST['text']
                message.save()
            except DatabaseError as e:
                print(f'Ошибка при сохранении сообщения в базу данных: {e.args}')
            else:
                return HttpResponseRedirect(reverse('users:message_list'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = MessageForm()

    content = {'title': title,
               'form': form,
               'message_id': message_id,
               **user_data}

    return render(request, 'userapp/reply_message.html', content)
