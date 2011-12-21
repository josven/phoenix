from django.utils.translation import ugettext_lazy as _
from django import forms

from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    message = forms.CharField(help_text=_('Message'), widget=forms.widgets.Textarea(attrs={
        'rows': 5,
    }))

    class Meta:
        model = Feedback
        exclude = ('user', 'site',)


