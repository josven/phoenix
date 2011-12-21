# -*- coding: utf-8 -*-
from models import *
from django import forms
from django.forms import ModelForm, Textarea, HiddenInput
from taggit.forms import *

class ArticleForm(ModelForm):
    """
    Form for articles

    """    

    tags = TagField(
        required=True,
        error_messages={
            'required': 'Du har inte angett någon kategori!',
        },
        widget=forms.HiddenInput,
    )
    
    class Meta:
        model = Article
        fields = ('title','body','tags',)
        widgets = {'body': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}),}
        
 
class ArticleBodyForm(ModelForm):

    class Meta:
        model = Article
        fields = ('body',)

        body = forms.CharField(label="", help_text="", widget=forms.Textarea())
