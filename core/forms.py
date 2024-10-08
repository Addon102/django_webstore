from .models import Product, Category, Comment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'short_description', 'full_description', 'image', 'category', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'price': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'place_holder': 'Введите ваше username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш пароль'
    }))

    class Meta:
        model = User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'place_holder': 'Введите ваше username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите ваш пароль'
    }))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше email'
            })
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }

