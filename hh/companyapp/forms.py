from django.forms import ModelForm
from django import forms
from django.forms.widgets import FileInput, CheckboxInput, Select, Textarea
from mainapp.models import Vacancy, CompanyProfile, News, Message


class CardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_name'].empty_label = "Выберите город"
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['activity_field'].widget.attrs.update({'rows': '3'})
        self.fields['other_info'].widget.attrs.update({'rows': '3'})

    class Meta:
        model = CompanyProfile
        widgets = {'logo': FileInput()}
        exclude = ['user_name', 'is_edu']


class VacancyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_name'].empty_label = "Выберите город"
        self.fields['education_type'].empty_label = "Ваше образование"
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['is_business_trip'].widget.attrs.update({'class': ''})
        self.fields['is_published'].widget.attrs.update({'class': ''})

        for field in ('category_name', 'city_name', 'type_of_employment', 'schedule',
                      'education_type', 'work_mode', 'relevance'):
            self.fields[field].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Vacancy
        exclude = ['user_name', 'publish_date']
        widgets = {'is_business_trip': CheckboxInput()}


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = News
        exclude = ['user_name', 'publication_date']
        widgets = {'photo': FileInput()}


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Message
        fields = ['text']
        widgets = {'text': Textarea}
