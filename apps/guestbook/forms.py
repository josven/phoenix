from models import *
from django.forms import ModelForm, Textarea, HiddenInput

class GuestbookForm(ModelForm):
    """
    Simple form for the guestbook

    """    
    class Meta:
        model = Guestbooks
        fields = ('text','user_id')
        widgets = {'text': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}),
                   'user_id':HiddenInput}