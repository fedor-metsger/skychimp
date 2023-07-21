
from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserActivationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ()
    user_code = forms.CharField(max_length=20,
                                label="Введите код из письма, присланного после регистрации:")