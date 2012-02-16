# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form, BooleanField
     
def update_entry_form(include_fields, form_model, *args, **kwargs):
    class TempForm(ModelForm):
        class Meta:
            model = form_model
            fields  = include_fields

        def __init__(self):
            super(TempForm, self).__init__(*args, **kwargs)

    return TempForm()
    
    
class delete_entry_form(Form):
    confirm = BooleanField(required=True, label="Vill du fortsätta?")