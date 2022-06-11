import hashlib
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DetailView, CreateView, DeleteView, ListView
from mainapp.tools import get_user_data, is_employer
from django.db import DatabaseError
from companyapp.forms import CardForm, VacancyForm, NewsForm, MessageForm
from mainapp.models import Users, Vacancy, Review, News, Message
from authapp.views import check_user
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
@is_employer
def card_edit(request):
    title = 'карточка компании/редактирование'

    user_data = get_user_data(request)

    if request.method == 'POST':
        edit_form = CardForm(request.POST, request.FILES, instance=user_data['company_profile'])
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('companies:card_edit'))
    else:
        edit_form = CardForm(instance=user_data['company_profile'])

    context = {'title': title,
               'edit_form': edit_form,
               **user_data}

    return render(request, 'companyapp/card_edit.html', context)


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'companyapp/vacancies.html'
    fields = '__all__'

    @method_decorator(is_employer)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @logger.catch
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context

    @logger.catch
    def get_queryset(self):
        # select vacancies by user by company:
        # print(f'self.request.user.id = {self.request.user.id}')
        # return Vacancy.objects.filter(company_name_id=4)  # self.request.user.id
        # Users.objects.get(pk=17).company_set.get().vacancy_set.all() # self.request.user.id
        # return Users.objects.get(pk=self.request.user.id).company_set.get().vacancy_set.all()  # self.request.user.id
        # return Users.objects.get(id=self.request.user.id).vacancy_set.all()
        # return Users.objects.get(id=self.request.session.get('user_id')).vacancy_set.all()
        return Vacancy.objects.filter(user_name_id=self.request.session.get('user_id'))


class VacancyCreateView(CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'companyapp/vacancy_create.html'
    success_url = reverse_lazy('companies:company_vacancies')

    @method_decorator(is_employer)
    # inherit parent 'dispatch' to apply decorator to the class:
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @logger.catch
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        instance = form.save(commit=False)
        instance.user_name_id = self.request.session.get('user_id')
        return super().form_valid(form)

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'companyapp/vacancy_show.html'

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'companyapp/vacancy_edit.html'
    success_url = reverse_lazy('companies:company_vacancies')

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'companyapp/vacancy_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('companies:company_vacancies')

    @logger.catch
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class ReviewListView(ListView):
    model = Review
    template_name = 'companyapp/review_list.html'

    @logger.catch
    def get_queryset(self):
        return Review.objects.filter(user_to_id=self.request.user.id)

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'companyapp/review_show.html'


@method_decorator(is_employer, name='dispatch')
class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'companyapp/news_create.html'
    success_url = reverse_lazy('companies:news')

    @logger.catch
    def form_valid(self, form):
        news = form.save(commit=False)
        news.user_name_id = self.request.session.get('user_id')
        return super().form_valid(form)

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class NewsListView(ListView):
    model = News
    template_name = 'companyapp/news.html'

    @logger.catch
    def get_queryset(self):
        return News.objects.filter(user_name_id=self.request.session.get('user_id'))

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class NewsDetailView(DetailView):
    model = News
    template_name = 'companyapp/news_show.html'

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'companyapp/news_edit.html'
    success_url = reverse_lazy('companies:news')

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context


@method_decorator(is_employer, name='dispatch')
class NewsDeleteView(DeleteView):
    model = News
    template_name = 'companyapp/news_delete.html'
    success_url = reverse_lazy('companies:news')

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request)
        context.update(**user_data)

        return context

    @logger.catch
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@logger.catch
@is_employer
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

    return render(request, 'companyapp/security.html', content)


@logger.catch
@is_employer
def message_list(request):
    title = 'Сообщения'

    user_data = get_user_data(request)
    messages = Message.objects.filter(Q(from_user_name_id=user_data['user'].id) | Q(to_user_name_id=user_data['user'].id)).order_by('-send_date')

    content = {'title': title,
               'messages': messages,
               **user_data}

    return render(request, 'companyapp/messages.html', content)


@logger.catch
@is_employer
def view_message(request, message_id):
    title = 'Просмотр сообщения # ' + str(message_id)

    user_data = get_user_data(request)

    content = {'title': title,
               'message': Message.objects.get(id=message_id),
               **user_data}

    return render(request, 'companyapp/view_message.html', content)


# @logger.catch
@is_employer
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
                return HttpResponseRedirect(reverse('companies:message_list'))
        else:
            print('Error while validation form data:', form.errors)
    else:
        form = MessageForm()

    content = {'title': title,
               'form': form,
               'message_id': message_id,
               **user_data}

    return render(request, 'companyapp/reply_message.html', content)
