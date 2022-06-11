from django.forms import ModelForm, RadioSelect
from django.forms.widgets import NumberInput, EmailInput, Textarea, FileInput
from mainapp.models import UserEdu, UserJobHistory, Resumes, Users, UserProfile, Message


class UserEduForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['edu_org_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['course_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['skills'].widget.attrs.update({'class': 'form-control'})
        self.fields['comments'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = UserEdu
        fields = ['edu_org_name', 'end_date', 'edu_type', 'course_name', 'skills', 'photo', 'comments']
        widgets = {'edu_type': RadioSelect(choices=UserEdu.EDU_CHOICES),
                   'photo': FileInput(),
                   'end_date': NumberInput(attrs={'type': 'date'})}


class UserJobHistoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in ['company_name', 'start_date', 'end_date', 'position', 'progress', 'comments']:
            self.fields[item].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = UserJobHistory
        fields = ['company_name', 'start_date', 'end_date', 'position', 'progress', 'comments']
        widgets = {'start_date': NumberInput(attrs={'type': 'date'}),
                   'end_date': NumberInput(attrs={'type': 'date'})}


class ResumeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in ['position_name', 'min_salary', 'comments']:
            self.fields[item].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Resumes
        fields = ['position_name', 'work_mode', 'min_salary', 'comments']
        widgets = {'work_mode': RadioSelect(choices=Resumes.WORK_MODE)}


class UserContactsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in ['email', 'comments']:
            self.fields[item].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Users
        fields = ['avatar', 'email', 'comments']
        widgets = {'email': EmailInput()}


class UserMainForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in ['last_name', 'first_name', 'middle_name', 'birth_date', 'phone_num', 'soft_skills',
                     'hard_skills', 'comments']:
            self.fields[item].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'middle_name', 'birth_date', 'phone_num', 'gender', 'soft_skills',
                  'hard_skills', 'comments']
        widgets = {'birth_date': NumberInput(attrs={'type': 'date'}),
                   'gender': RadioSelect(choices=UserProfile.GENDER_CHOICES),
                   'soft_skills': Textarea(),
                   'hard_skills': Textarea(),
                   'comments': Textarea()}


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Message
        fields = ['text']
        widgets = {'text': Textarea}
