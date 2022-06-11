from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authapp.models import Users


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('role_name', 'username', 'email', 'avatar')  # , 'role_name

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['role_name'].empty_label = "Выберите роль"
        self.fields['username'].label = "Логин"
        self.fields['email'].label = "Email"
        self.fields['role_name'].label = ""
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтвердите пароль"
        self.fields['avatar'].label = "Аватар"

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = Users
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
