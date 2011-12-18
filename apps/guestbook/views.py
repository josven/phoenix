# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User, Group
from apps.core.utils import render
from forms import *

def guestbook(request,userid,start=None):
    """
    Guestbook
    
    """
    
    increment = int(10) 
    padding = int(1)
    
    if start == None:
        start = int(0)

    posts = Guestbooks.active.filter(user_id=userid).order_by('-date_created')[start:int(start)+increment+padding]

    form = GuestbookForm()
    vars = {
            'form':form,
            'posts':posts,
            'start':start,
            'increment':increment,
            'negincrement':-increment,
            'padding':padding,
            'user_id':userid
            }
    
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['user_id'] = str(userid)
        form = GuestbookForm(post_values)
        if form.is_valid():
            form.save()
        else:
            messages.add_message(request, messages.INFO, 'Nu blev det något fel')


    return render(request, 'guestbook.html', vars )
