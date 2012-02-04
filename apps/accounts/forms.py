# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

class AccountForm(ModelForm):
    #fields = ('password','username',)
    
    class Meta:
        model = User