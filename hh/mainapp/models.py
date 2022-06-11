from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime


def check_rate(value):
    if value not in [1, 2, 3, 4, 5]:
        raise ValidationError('Error value in rate field')


def check_gender(value):
    if value not in [1, 2]:
        raise ValidationError('Error value in gender field')


def check_edu_choices(value):
    if value not in [1, 2, 3]:
        raise ValidationError('Error value in edu_choice field')


def check_rus_letters_only(value):
    for char in value:
        if char.lower() not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            raise ValidationError('Must be russian letters only')


def check_digits_only(value):
    for char in str(value):
        if char not in '+0123456789':
            raise ValidationError('Must be digit or plus symbol only')


def check_end_date(value):
    if value == '':
        return None
    else:
        if not isinstance(value, datetime.date):
            raise ValidationError(value, 'value has an invalid date format. It must be in YYYY-MM-DD format.')


class City(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=100, unique=True, blank=False)

    class Meta:
        db_table = 'City'
        verbose_name = 'Населенные пункты'

    def __str__(self):
        return self.name


class Roles(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=50, unique=True, blank=False)
    comments = models.TextField(verbose_name='Примечание', blank=True)

    class Meta:
        db_table = 'Roles'
        verbose_name = 'Роли пользователей'

    def __str__(self):
        return self.name


class Users(models.Model):
    login = models.CharField(verbose_name='Логин', max_length=50, unique=True, blank=True)
    hash_password = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    email = models.CharField(verbose_name='e-mail', max_length=100, validators=[EmailValidator])
    role_name = models.ForeignKey(Roles, on_delete=models.RESTRICT, null=True)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=now()+timedelta(hours=48))
    comments = models.CharField(verbose_name='Примечание', max_length=100, blank=True)

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователи'

    def __str__(self):
        return self.login

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class UserProfile(models.Model):
    MALE = 'Мужской'
    FEMALE = 'Женский'

    GENDER_CHOICES = (
        (1, MALE),
        (2, FEMALE),
    )

    GENDER_DICT = {
        1: MALE,
        2: FEMALE
    }

    user_name = models.OneToOneField(Users, unique=True, null=False, db_index=True, on_delete=models.RESTRICT)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=False,
                                 validators=[check_rus_letters_only])
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=False, validators=[check_rus_letters_only])
    middle_name = models.CharField(verbose_name='Отчество', max_length=50, blank=False,
                                   validators=[check_rus_letters_only])
    birth_date = models.DateField(verbose_name='Дата рождения', null=True)
    phone_num = models.CharField(verbose_name='Телефоны', max_length=100, validators=[check_digits_only])
    city_name = models.ForeignKey(City, on_delete=models.RESTRICT, null=True)
    home_address = models.CharField(verbose_name='Домашний адрес', max_length=150, blank=True)
    gender = models.IntegerField(verbose_name='Пол', choices=GENDER_CHOICES, default=1, validators=[check_gender])
    soft_skills = models.TextField(verbose_name='soft skills', blank=True)
    hard_skills = models.TextField(verbose_name='hard skills', blank=True)
    comments = models.TextField(verbose_name='Дополнительные сведения', blank=True)

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'Профиль пользователя'

    def __str__(self):
        return ' '.join([self.last_name, self.first_name, self.last_name])


class CompanyProfile(models.Model):
    user_name = models.OneToOneField(Users, unique=True, null=False, db_index=True, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name='Наименование', max_length=200, unique=True, blank=False)
    description = models.TextField(verbose_name='Приветственное письмо', max_length=400, null=True)
    activity_field = models.TextField(verbose_name='Сфера деятельности', max_length=400, null=True)
    other_info = models.TextField(verbose_name='Другая информация', max_length=400, blank=True)
    site = models.URLField(verbose_name='Сайт', max_length=200, blank=True)
    short_name = models.CharField(verbose_name='Короткое наименование', max_length=20)
    is_edu = models.BooleanField(verbose_name='Образовательное учреждение', null=True)
    logo = models.ImageField(verbose_name='Логотип компании', upload_to='avatars', blank=True)
    city_name = models.ForeignKey(City, verbose_name='Город места нахождения', on_delete=models.RESTRICT, null=True)
    comments = models.CharField(verbose_name='Примечание', max_length=100, blank=True)

    class Meta:
        db_table = 'CompanyProfile'
        verbose_name = 'Профиль компании'

    def get_absolute_url(self):
        return reverse('companies:card_show', kwargs={'id': self.id})

    def __str__(self):
        return self.name


class UserEdu(models.Model):
    HIGHER_EDUCATION = 'Высшее образование'
    SECONDARY_SPECIAL_EDUCATION = 'Среднее специальное образование'
    PROFESSIONAL_EDUCATION = 'Повышение квалификации / Переквалификация'

    EDU_CHOICES = (
        (1, HIGHER_EDUCATION),
        (2, SECONDARY_SPECIAL_EDUCATION),
        (3, PROFESSIONAL_EDUCATION),
    )
    EDU_DICT = {
        1: HIGHER_EDUCATION,
        2: SECONDARY_SPECIAL_EDUCATION,
        3: PROFESSIONAL_EDUCATION,
    }

    user_name = models.ForeignKey(Users, on_delete=models.RESTRICT)
    edu_org_name = models.CharField(verbose_name='Учебное заведение', max_length=100, blank=False, default='')
    end_date = models.DateField(verbose_name='Дата окончания', null=False)
    edu_type = models.IntegerField(verbose_name='Уровень образования', choices=EDU_CHOICES, default=1,
                                   validators=[check_edu_choices])
    course_name = models.CharField(verbose_name='Факультет/Курс (для переквалификации)', max_length=100, blank=True)
    skills = models.CharField(verbose_name='Полученная профессия/специальность', max_length=100, blank=True)
    photo = models.ImageField(verbose_name='Фото документа об образовании', upload_to='docs', blank=True)
    comments = models.CharField(verbose_name='Примечание', max_length=100, blank=True, default='')

    class Meta:
        db_table = 'UserEdu'
        verbose_name = 'Образование'


class UserJobHistory(models.Model):
    user_name = models.ForeignKey(Users, on_delete=models.RESTRICT)
    company_name = models.CharField(verbose_name='Организация', max_length=100, blank=True)
    start_date = models.DateField(verbose_name='Дата начала работы', blank=False)
    end_date = models.DateField(verbose_name='Дата окончания работы', blank=True, null=True,
                                validators=[check_end_date])
    position = models.CharField(verbose_name='Должность', max_length=50, blank=True)
    progress = models.TextField(verbose_name='Результат / достижения', blank=True)
    comments = models.CharField(verbose_name='Примечание', max_length=100, blank=True)

    class Meta:
        db_table = 'UserJobHistory'
        verbose_name = 'Трудовая деятельность'


class Articles(models.Model):
    header = models.CharField(verbose_name='Заголовок статьи', max_length=100, blank=False)
    text = models.TextField(verbose_name='Содержание статьи', blank=True)
    url = models.CharField(verbose_name='Ссылка на статью', max_length=100, blank=True)
    user_name = models.ForeignKey(Users, on_delete=models.RESTRICT)
    publish_date = models.DateField(verbose_name='Дата публикации', null=True)

    class Meta:
        db_table = 'Articles'
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.header + ' ' + self.text[:100] + '...'


class Categories(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=50, blank=True, unique=True)

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категории вакансий'
        verbose_name_plural = 'Категории вакансий'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    FULL_TIME = 'Полный рабочий день'
    PARTIAL_TIME = 'Частичная занятость'
    REMOTE = 'Удаленное место работы'
    SHIFT_METHOD = 'Вахтовый метод работы'
    PROJECT_MODE = 'Проектная работа'

    WORK_MODE = (
        (1, FULL_TIME),
        (2, PARTIAL_TIME),
        (3, REMOTE),
        (4, SHIFT_METHOD),
        (5, PROJECT_MODE),
    )

    TYPE_OF_EMPLOYMENT = [
        (1, 'Полная занятость'),
        (2, 'Частичная занятость'),
        (3, 'Проектная работа'),
        (4, 'Стажировка'),
        (5, 'Волонтерство'),
    ]

    SCHEDULE = [
        (1, 'Полный день'),
        (2, 'Гибкий график'),
        (3, 'Удаленная работа'),
        (4, 'Сменный график'),
        (5, 'Вахтовый метод'),
    ]

    EXPERIENCE = [
        (1, 'Не имеет значения'),
        (2, 'Нет опыта'),
        (3, 'От 1 года до 3 лет'),
        (4, 'От 3 до 6 лет'),
        (5, 'Более 6 лет'),
    ]

    ANSWER = [
        (1, 'Да'),
        (2, 'Нет'),
    ]

    RELEVANCE = [
        (1, 'active'),
        (2, 'closed')
    ]

    user_name = models.ForeignKey(Users, on_delete=models.RESTRICT)
    category_name = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.RESTRICT, null=True)
    position_name = models.CharField(verbose_name='Должность', max_length=50, blank=False)
    city_name = models.ForeignKey(City, verbose_name='Город места нахождения вакансии', on_delete=models.RESTRICT)
    work_experience = models.CharField(verbose_name='Опыт работы', max_length=50, blank=True)
    type_of_employment = models.IntegerField(verbose_name='Тип занятости', choices=TYPE_OF_EMPLOYMENT, default=1)
    schedule = models.IntegerField(verbose_name='График работы', choices=SCHEDULE, default=1)
    description = models.TextField(verbose_name='Описание', max_length=1000, blank=True)
    is_business_trip = models.BooleanField(verbose_name='Готовность к командировкам', default=False)
    education_type = models.IntegerField(verbose_name='Образование', choices=UserEdu.EDU_CHOICES, default=1)
    relevance = models.IntegerField(verbose_name='Актуальность вакансии', choices=RELEVANCE, default=1)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовать")
    work_mode = models.IntegerField(verbose_name='Тип занятости', choices=WORK_MODE, default=1)
    requirements = models.TextField(verbose_name='Требования к кандидату', blank=True)
    min_salary = models.IntegerField(verbose_name='Минимальная ЗП', null=True)
    conditions = models.TextField(verbose_name='Условия работы', blank=True)
    publish_date = models.DateField(verbose_name='Дата публикации', null=True)

    class Meta:
        db_table = 'Vacancy'
        verbose_name = 'Вакансии'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.position_name


class Review(models.Model):
    user_from = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='user_from',
                                  verbose_name='Чей отзыв', blank=False)
    user_to = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='user_to',
                                verbose_name='О ком отзыв', blank=False)
    content = models.TextField(verbose_name='Отзыв', max_length=1000, blank=False)
    rate = models.IntegerField(verbose_name='Оценка компании', null=False, default=1, validators=[check_rate])
    publication_date = models.DateTimeField(verbose_name='Дата публикации', auto_now=True)

    def __str__(self):
        return f'Отзыв от {self.user_from}'

    class Meta:
        db_table = 'Review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class News(models.Model):
    user_name = models.ForeignKey(Users, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    photo = models.ImageField(upload_to='photo_news', verbose_name='Сопровождающее изображение', blank=True)
    content = models.TextField(verbose_name='Содержание', max_length=1000)
    publication_date = models.DateField(verbose_name='Дата публикации', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'News'
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class Resumes(models.Model):
    FULL_TIME = 'Полный рабочий день'
    PARTIAL_TIME = 'Частичная занятость'
    REMOTE = 'Удаленное место работы'
    SHIFT_METHOD = 'Вахтовый метод работы'
    PROJECT_MODE = 'Проектная работа'

    WORK_MODE = (
        (1, FULL_TIME),
        (2, PARTIAL_TIME),
        (3, REMOTE),
        (4, SHIFT_METHOD),
        (5, PROJECT_MODE),
    )
    WORK_MODE_DICT = {
        1: FULL_TIME,
        2: PARTIAL_TIME,
        3: REMOTE,
        4: SHIFT_METHOD,
        5: PROJECT_MODE,
    }
    user_name = models.ForeignKey(Users, on_delete=models.RESTRICT)
    position_name = models.CharField(verbose_name='Должность', max_length=50, blank=False)
    work_mode = models.IntegerField(verbose_name='Тип занятости', choices=WORK_MODE, default=1)
    min_salary = models.IntegerField(verbose_name='Желаемая ЗП', null=True)
    publish_date = models.DateField(verbose_name='Дата публикации', null=True, auto_now_add=True)
    comments = models.CharField(verbose_name='Примечание', max_length=100, blank=True)

    class Meta:
        db_table = 'Resumes'
        verbose_name = 'Резюме соискателей'
        verbose_name_plural = 'Резюме соискателей'


class Message(models.Model):
    reply_to_message = models.ForeignKey('Message', on_delete=models.RESTRICT, null=True)
    from_user_name = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='sender',
                                       verbose_name='Сообщение от', blank=False)
    to_user_name = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='receiver',
                                     verbose_name='Сообщение для', blank=False)
    text = models.TextField(verbose_name='Сообщение', max_length=1000, blank=False)
    send_date = models.DateTimeField(verbose_name='Дата отправления', auto_now=True)

    def __str__(self):
        return f'Сообщение от {self.from_user_name}'

    class Meta:
        db_table = 'Message'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
