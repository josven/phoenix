# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturalday

from apps.core.utils import render, get_datatables_records

from forms import *
from models import Users


@never_cache
@login_required(login_url='/auth/login/')
def list_accounts(request):
    
    vars = {}
    
    return render(request,'list_accounts.html', vars)


@never_cache
@login_required(login_url='/auth/login/')
def list_accounts_json(request):

    if request.is_ajax():

        #initial querySet 
        querySet = Users.objects.all()

        #columnIndexNameMap is required for correct sorting behavior
        columnIndexNameMap = { 
                                0: 'profile__photo',
                                1: 'username',
                                2: 'last_login',
                                3: 'date_joined',
                                4: 'profile__gender',
                                5: 'profile__location',
                                6: 'profile__birthdate',
                            }

        #call to generic function from utils
        return get_datatables_records(request, querySet, columnIndexNameMap)

    raise Http404 
    
@never_cache
@login_required(login_url='/auth/login/')
def update_account(request):
    """
    Update account settings
    
    """
    forms = [
                
            ]
                
    vars = {
            'username_change_form': UsernameChangeForm(instance = request.user, prefix='UsernameChangeForm'),
            'password_change_form': PasswordChangeForm(request.user, prefix='PasswordChangeForm')
            }
    if request.method == 'GET':
        profile = request.user.get_profile()
        if profile.date_username_last_changed:
            delta = datetime.now() - profile.date_username_last_changed
            if delta < timedelta(weeks=8):
                next_update = profile.date_username_last_changed + timedelta(weeks=8)
                
                str_next_update = u"{0}, {1}".format( naturalday( next_update ), next_update.strftime("%H:%M") )
                str_date_username_last_changed = u"{0}, {1}".format( naturalday( profile.date_username_last_changed ), profile.date_username_last_changed.strftime("%H:%M") )
                
                vars['time_username_change_message'] = u"Du böt användarnamn: {0} och måste vänta tills {1} för att byta igen".format(str_date_username_last_changed ,str_next_update)
        
    if request.method == 'POST':
        
        if 'username_change_form' in request.POST:
            username_change_form = UsernameChangeForm(request.POST, prefix='UsernameChangeForm')
            if username_change_form.is_valid():
                #username_change_form.save()
                username = username_change_form.cleaned_data['username']
                user = request.user
                profile = user.get_profile()
                
                cond_username_avail = True
                try:
                    another_user = User.objects.get(username__iexact=username)
                    messages.add_message(request, messages.INFO, "Användarnamn upptaget.")
                    cond_username_avail = False
                except:
                    pass
                
                cond_time_passed = True
                if profile.date_username_last_changed:
                    delta = datetime.now() - profile.date_username_last_changed
                    if delta < timedelta(weeks=8):
                        cond_time_passed = False
                        messages.add_message(request, messages.INFO, "Du kan inte ändra användarnamn just nu.")
                
                if cond_username_avail and cond_time_passed:
                    user.username = username
                    user.save()
                    profile.date_username_last_changed = datetime.now()
                    profile.save()
                    messages.add_message(request, messages.INFO, "Användarnamn ändrat.")
                    
            vars['username_change_form'] = username_change_form
            
        if 'password_change_form' in request.POST:
            password_change_form = PasswordChangeForm(request.user, request.POST, prefix='PasswordChangeForm')
            if password_change_form.is_valid():
                password_change_form.save()
                messages.add_message(request, messages.INFO, "Lösenord ändrat.")
            vars['password_change_form'] = password_change_form
            
    return render(request,'update_account.html', vars)
    

 

 
class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None