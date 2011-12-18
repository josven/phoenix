# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from models import Profile
from apps.core.utils import create_datepicker

class ProfileForm(ModelForm):
    formfield_callback = create_datepicker
    class Meta:
        model = Profile
        exclude = ('user')
