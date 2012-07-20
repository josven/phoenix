# -*- coding: utf-8 -*-

from models import *
from django.forms import ModelForm, Textarea, HiddenInput, CharField, BooleanField
import site_strings

class GuestbookForm(ModelForm):
    """
    Simple form for the guestbook

    """

    text = CharField(label="", widget=Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}), help_text=site_strings.COMMENT_FORM_HELP_TEXT)

    class Meta:
        model = Guestbooks
        fields = ('text','user_id')
        widgets = {'user_id':HiddenInput}


class DeleteGuestbookForm(ModelForm):
    """
    Simple form for the guestbook

    """

    confirm = BooleanField(label=u'Bekräfta')

    class Meta:
        model = Guestbooks
        fields = ('confirm',)
        #widgets = {'id':HiddenInput}