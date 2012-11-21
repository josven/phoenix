# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm as DjangoAuthenticationForm
from django import forms
from django.contrib.auth.models import User

import site_strings

from apps.mobile.widgets import TextInput
from apps.chat.models import Post as ChatPost
from apps.mobile.models import mobile_settings

class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(label = "Email")

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username__iexact=data).exists():
            raise forms.ValidationError( u"Det finns redan användare som heter {0}".format(data))
        return data

class AuthenticationForm(DjangoAuthenticationForm):
    keep_session = forms.BooleanField(required=False, label='Håll mig inloggad')


class ChatForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.TextInput(), help_text=site_strings.COMMENT_FORM_HELP_TEXT)
    text.widget = forms.TextInput(attrs={'data-mini': 'true','placeholder': 'Skriv här...'})

    class Meta:
        model = ChatPost
        fields = ('text',)


class ChatSettingsForm(forms.ModelForm):
    class Meta:
        model = mobile_settings
        fields = ('chat_textile','chat_oembed','chat_urlize',)