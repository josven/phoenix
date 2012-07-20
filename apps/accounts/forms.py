# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

class UsernameChangeForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username',)

class EmailChangeForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('email',)