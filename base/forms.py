from django import forms
from django.forms.models import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "email",
            "password1",
            "password2"
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'avatar', 'bio']
