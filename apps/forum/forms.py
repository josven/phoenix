# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from taggit.forms import *
from models import *
                            
DEFAULT_CATEGORIES = ( (tag, unicode( tag ).title() ) for tag in defaultCategories.objects.all() )
               
class DefaultForumTagsForm(forms.Form):
    default_tags = forms.MultipleChoiceField(
        required=True,
        widget=CheckboxSelectMultiple(attrs={'class':'ui-tag-reformat'}),
        choices=DEFAULT_CATEGORIES
    )

class ForumForm(ModelForm):
    """
    Form for articles

    """    

    tags = TagField(
        required=False,
        error_messages={
            'required': 'Du har inte angett någon kategori!',
        },
        widget=TagWidget(attrs={'placeholder': 'Egna kategorier, separera dem med comma (,)'}),
        label = "",
    )
    
    class Meta:
        model = Forum
        fields = ('title','body','tags',)
        widgets = {'title': forms.TextInput(attrs={'placeholder': "Ange en titel"}), 
		'body': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."})}

class ForumCommentForm(ModelForm):

    class Meta:
        model = ForumComment
        fields = ('comment',)
        
''' ######################### OLD ############################# '''    
class ThreadForm(forms.Form):
    title_min = 5
    title_max = 100

    title = forms.CharField(
        required=True,
        label="",
        min_length=title_min,
        max_length=title_max,
        widget=forms.TextInput(attrs={'placeholder': 'Titeln måste vara minst %s tecken lång.' % title_min}),
        error_messages={
            'required': 'Du har inte angett en titel!',
            'min_length': 'Titeln måste vara minst %s tecken lång.' % title_min,
        }
    )
    
    tags = TagField(
        required=False,
        error_messages={
            'required': 'Du har inte angett någon kategori!',
        },
        widget=TagWidget(attrs={'placeholder': 'Egna kategorier, separera dem med comma (,)'}),
        label = "",
    )
    
    body = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder': "Skriv ditt meddelande"}),
        error_messages={
            'required': 'Du måste fylla i detta fält.',
        }
    )


class ForumPostForm(forms.Form):
    thread_id = forms.IntegerField()
    parent_id = forms.IntegerField()
    body = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Fortsätt på tråden:'}),
        required=True,
        error_messages={
            'required': 'Du måste fylla i detta fält.',
        }
    )