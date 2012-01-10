# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from sorl.thumbnail import ImageField

from models import Profile
from apps.core.utils import create_datepicker

class ProfileForm(ModelForm):
    formfield_callback = create_datepicker
    
    class Meta:
        model = Profile
        exclude = ('user')
        description = forms.CharField(help_text="Formateringshjälp: http://sv.wikipedia.org/wiki/Textile")
        
class ProfileDescriptionForm(ModelForm):
    formfield_callback = create_datepicker
    class Meta:
        model = Profile
        fields = ('description',)

        description = forms.CharField(label="", help_text="", widget=forms.Textarea())
