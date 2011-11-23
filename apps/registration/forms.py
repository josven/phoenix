from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label = "Email",
        widget=forms.TextInput(attrs={ 'placeholder': 'Epost' }),
        )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={ 'placeholder': 'Användarnamn' })
        )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'placeholder': 'Lösenord' })
        )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'placeholder': 'Lösenord igen' })
        )

    class Meta:
        model = User
        fields = ("username", "email")
