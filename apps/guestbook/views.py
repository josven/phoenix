# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from apps.core.utils import render
from forms import *

@never_cache
@login_required(login_url='/auth/login/')
def guestbook(request,userid,start=None):
    """
    Guestbook
    
    """
    
    user = User.objects.get(pk=userid)
    
    increment = int(10) 
    padding = int(1)
    
    if start == None:
        start = int(0)

    posts = Guestbooks.active.filter(user_id=user.id).order_by('-date_created')[start:int(start)+increment+padding]

    form = GuestbookForm()
    vars = {
            'form':form,
            'posts':posts,
            'start':start,
            'increment':increment,
            'negincrement':-increment,
            'padding':padding,
            'user_id':user.id,
            'user':user,
            'profile':user.get_profile()
            }
    
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['user_id'] = str(userid)
        form = GuestbookForm(post_values)
        if form.is_valid():
            form.save()
        else:
            messages.add_message(request, messages.INFO, 'Nu blev det något fel')

    if request.is_ajax():
        template = "_guestbook.html"
    else:
        template = "guestbook.html"

    return render(request, template, vars )
