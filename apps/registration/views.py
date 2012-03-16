﻿from datetime import timedelta

from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from models import BetaReg
from apps.profiles.models import Profile

from apps.core.utils import render

@never_cache
def auth_login(request):
    """
    Log in a user
    
    """
    vars = {
        'body_id':'page_login'
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            '''
            if not user.is_staff:
                messages.add_message(request, messages.INFO, "Siten inte öppen.")
                return render(request, 'comming_soon.html')
            '''
            
            if user.is_active:
                
                login(request, user)
                
                if request.POST.get('keepsession', None):
                    request.session.set_expiry(timedelta(days=365))
                else:
                    request.session.set_expiry(0)

                return HttpResponseRedirect(reverse('start'))
                
            else:
                messages.add_message(request, messages.INFO, "Ej aktiv användare")
        else:
            messages.add_message(request, messages.INFO, "Fel användarnamn eller lösenord.")

    return render(request, 'login.html')

@login_required(login_url='/auth/login/')
def auth_logout(request):
    """
    Log out a user
    
    """
    logout(request)
    return render(request, 'login.html')


def auth_register(request):
    """
    register a user
    
    """
    
    #return render(request,'comming_soon.html')
    
    
    vars = {
        'body_id':'page_register'
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            try:
                User.objects.get(username__iexact=username)
                vars['form'] = form
                messages.add_message(request, messages.INFO, "Användare {0} finns redan.".format( unicode( username ) ) )
                return render(request, 'register.html', vars)
            
            except:
                form.save()
                form = AuthenticationForm()
                messages.add_message(request, messages.INFO, "Användare skapad.")
                user = authenticate(username=username, password=password)
                login(request, user)
                profile, created = Profile.objects.select_related().get_or_create(user=user)
                
                return HttpResponseRedirect(reverse('start'))
                
        else:
            messages.add_message(request, messages.INFO, "Fel fel fel fel")
    else:
        form = RegisterForm()

    vars['form'] = form
    return render(request, 'register.html', vars)