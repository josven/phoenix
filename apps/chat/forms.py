from models import *
from django.forms import ModelForm, Textarea

class PostForm(ModelForm):
    """
    Simple form for the chat

    """    
    class Meta:
        model = Post
        fields = ('text',)
        widgets = {'text': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': "Minst fem tecken."}),}