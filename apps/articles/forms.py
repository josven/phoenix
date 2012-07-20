# -*- coding: utf-8 -*-
from models import *
from django import forms
from django.forms import ModelForm, Textarea, HiddenInput, CheckboxInput
from django.forms.fields import MultipleChoiceField
from apps.core.widgets import CheckboxSelectMultiple

import site_strings

from taggit.forms import *

DEFAULT_CATEGORIES = ( (tag, unicode( tag ).title() ) for tag in defaultArticleCategories.objects.all() )

class DefaultArticleTagsForm(forms.Form):
    default_tags = forms.MultipleChoiceField(
        required=True,
        widget=CheckboxSelectMultiple(attrs={'class':'ui-toggle-button'}),
        choices=DEFAULT_CATEGORIES,
        label="Huvudkategorier",
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

        super(ArticleForm, self).__init__(*args, **kwargs)
        if user is not None:
            subscriptions =  user.profile.subscriptions.all()
            subscriptions_choices = ( (tag, unicode( tag ).title() ) for tag in subscriptions )
            self.fields['user_tags'].choices = subscriptions_choices

    class Meta:
        model = Article
        fields = ('user_tags','tags','title','body','allow_comments',)
        widgets = {
                    'title': forms.TextInput(attrs={'placeholder': "Ange en titel"}),
		            'body': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}),
                    'allow_comments':CheckboxInput(),
                   }
        
 
class ArticleBodyForm(ModelForm):

    class Meta:
        model = Article
        fields = ('body',)

        body = forms.CharField(label="", help_text="", widget=forms.Textarea())

class ArticleCommentForm(ModelForm):
    comment = forms.CharField(label="", widget=forms.Textarea(), help_text=site_strings.COMMENT_FORM_HELP_TEXT)

    class Meta:
        model = ArticleComment
        fields = ('comment',)
