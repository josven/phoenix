# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm as DjangoAuthenticationForm
from django import forms
from django.contrib.auth.models import User

class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(label = "Email")

class AuthenticationForm(DjangoAuthenticationForm):
    keep_session = forms.BooleanField(required=False, label='Håll mig inloggad')
        