# -*- coding: utf-8 -*-
from datetime import timedelta

from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from forms import AuthenticationForm, UserCreationForm

from apps.profiles.models import Profile

from apps.core.utils import render

@never_cache
def startpage(request):
    """
    Startpage for PHX
    """

    if request.user.is_authenticated():
        return HttpResponseRedirect( reverse('start') )

    vars = {
        'body_id':'page_startpage',
        'AuthenticationForm': AuthenticationForm(),
        'UserCreationForm': UserCreationForm(),
        'nextpage': request.GET.get('next', reverse('start')),
    }

    return render(request, 'startpage.html',vars)


@never_cache
def auth_reset_password(request):
    """
    reset user password
    """
    vars = {
        'PasswordResetForm':PasswordResetForm( data = request.POST or None ),
    }

    if request.method == 'POST':
        if vars['PasswordResetForm'].is_valid():
            vars['PasswordResetForm'].save()

    return render(request, 'reset_password.html', vars)

@never_cache
def auth_login(request):
    """
    Log in a user
    
    """
    vars = {
        'body_id':'page_login',
        'AuthenticationForm': AuthenticationForm( data = request.POST or None ),
        'nextpage': request.GET.get('next', reverse('start')),
    }

    if request.method == 'POST':
        if vars['AuthenticationForm'].is_valid():
            user = vars['AuthenticationForm'].get_user()

            if user.is_active:
                login(request, user)

                if request.POST.get('keep_session', None):
                    request.session.set_expiry(timedelta(days=365))
                else:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(vars['nextpage'])

    return render(request, 'login.html', vars)

@login_required()
def auth_logout(request):
    """
    Log out a user
    
    """
    logout(request)
    return HttpResponseRedirect( reverse('startpage') )


def auth_register(request):
    """
    register a user
    
    """
    
    #return render(request,'comming_soon.html')
    
    
    vars = {
        'body_id':'page_register',
        'UserCreationForm': UserCreationForm( data = request.POST or None ),
        'nextpage': request.GET.get('next', reverse('start')),
    }

    if request.method == 'POST':
        if vars['UserCreationForm'].is_valid():
            
            username = vars['UserCreationForm'].cleaned_data['username']
            password = vars['UserCreationForm'].cleaned_data['password1']

            # Try/except är en koll för att kolla om det redan finns en användare med samma namn             
            try:
                User.objects.get(username__iexact=username)
                return render(request, 'register.html', vars)
            except:
                vars['UserCreationForm'].save()
                user = authenticate(username=username, password=password)
                login(request, user)
                profile, created = Profile.objects.get_or_create(user=user)
                return HttpResponseRedirect(vars['nextpage'])

    return render(request, 'register.html', vars)