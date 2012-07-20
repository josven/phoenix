from models import *
from django.forms import ModelForm, Textarea, CharField
import site_strings

class PostForm(ModelForm):
    """
    Simple form for the chat

    """

    text = CharField(label="", widget=Textarea(), help_text=site_strings.COMMENT_FORM_HELP_TEXT)

    class Meta:
        model = Post
        fields = ('text',)
        widgets = {'text': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}),}