from django import forms

class update_entry_form(forms.Form):
    content = forms.CharField(label="", help_text="", widget=forms.Textarea())