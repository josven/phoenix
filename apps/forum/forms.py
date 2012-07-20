# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField
from django.forms.fields import MultipleChoiceField
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from apps.core.widgets import CheckboxSelectMultiple

from taggit.forms import *
from models import *
from apps.notifications.models import Notification
import site_strings

DEFAULT_CATEGORIES = ( (tag, unicode( tag ).title() ) for tag in defaultCategories.objects.all() )

class DefaultForumTagsForm(forms.Form):
    default_tags = forms.MultipleChoiceField(
        required=True,
        widget=CheckboxSelectMultiple(attrs={'class':'ui-toggle-button'}),
        choices=DEFAULT_CATEGORIES,
        label="Huvudkategorier",
    )

class ForumForm(ModelForm):
    """
    Form for Forumposts

    """    

    tags = TagField(
        required=False,
        error_messages={
            'required': 'Du har inte angett någon kategori!',
        },
        widget=TagWidget(attrs={'placeholder': 'Egna kategorier, separera dem med kommatecken (,)'}),
        label="Egna kategorier",
        help_text="Separera kategorier med kommatecken. Kategorier med flera ord skrivs inom fnuttar."
    )
    
    user_tags = forms.MultipleChoiceField(
        required=False,
        widget=CheckboxSelectMultiple(),
        choices=DEFAULT_CATEGORIES,
        label="Egna bevakade kategorier",
    )

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)

        super(ForumForm, self).__init__(*args, **kwargs)
        if user is not None:
            subscriptions =  user.profile.subscriptions.all()
            subscriptions_choices = ( (tag, unicode( tag ).title() ) for tag in subscriptions )
            self.fields['user_tags'].choices = subscriptions_choices


    class Meta:
        model = Forum
        fields = ('user_tags','tags','title','body',)
        widgets = {'title': forms.TextInput(attrs={'placeholder': "Ange en titel"}), 
		'body': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."})}

class ForumCommentForm(ModelForm):
    
    comment = forms.CharField(label="", widget=forms.Textarea(), help_text=site_strings.COMMENT_FORM_HELP_TEXT)

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
        widget=TagWidget(attrs={'placeholder': 'Egna kategorier, separera dem med kommatecken (,)'}),
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