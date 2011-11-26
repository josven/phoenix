# -*- coding: utf-8 -*-
from django import forms

class ThreadForm(forms.Form):
    title_min = 10
    title_max = 100

    title = forms.CharField(
        required=True,
        min_length=title_min,
        max_length=title_max,
        error_messages={
            'required': 'Du har inte angett en titel!',
            'min_length': 'Titeln måste vara minst %s tecken lång.' % title_min,
        }
    )