from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import UserProfile, Article


class RegisterForm(UserCreationForm):
    USER_TYPES = (
        ('READER', 'Reader'),
        ('EDITOR', 'Editor'),
        ('JOURNALIST', 'Journalist'))
    email = forms.EmailField()
    user_type = forms.CharField(widget=forms.Select(
        choices=USER_TYPES,
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    pass


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content',]