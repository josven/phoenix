# -*- coding: utf-8 -*-
from models import *
from django import forms
from django.forms import ModelForm, Textarea, HiddenInput, CheckboxInput
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from taggit.forms import *

DEFAULT_CATEGORIES = ( (tag, unicode( tag ).title() ) for tag in defaultArticleCategories.objects.all() )

class DefaultArticleTagsForm(forms.Form):
    default_tags = forms.MultipleChoiceField(
        required=True,
        widget=CheckboxSelectMultiple(attrs={'class':'ui-tag-reformat'}),
        choices=DEFAULT_CATEGORIES
    )
    
class ArticleForm(ModelForm):
    """
    Form for articles

    """    

    tags = TagField(
        required=False,
        error_messages={
            'required': 'Du har inte angett någon kategori!',
        },
        widget=TagWidget(attrs={'placeholder': 'Egna kategorier, separera dem med kommatecken (,)'}),
        label = "",
    )
    
    class Meta:
        model = Article
        fields = ('title','body','tags','allow_comments',)
        widgets = {'title': forms.TextInput(attrs={'placeholder': "Ange en titel"}),
		'body': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}),
                   'allow_comments':CheckboxInput()}
        
 
class ArticleBodyForm(ModelForm):

    class Meta:
        model = Article
        fields = ('body',)

        body = forms.CharField(label="", help_text="", widget=forms.Textarea())

class ArticleCommentForm(ModelForm):

    class Meta:
        model = ArticleComment
        fields = ('comment',)
