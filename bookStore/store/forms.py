from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from . import models


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ReviewForm(forms.ModelForm):
    text = forms.CharField(label='Отзыв', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'maxlength': '250',
    }))

    class Meta:
        model = models.Review
        fields = ('text',)


class OrderForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=models.Book.objects.all(),
        label='Книга',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.Order
        fields = ('book',)