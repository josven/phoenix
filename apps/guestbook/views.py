# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from apps.core.utils import render
from forms import *

from apps.notifications.models import Notification
 
@never_cache
@login_required(login_url='/auth/login/')
def guestbook(request,userid,start=None, id=None):
    """
    Guestbook
    
    """
    
    user = User.objects.get(pk=userid)
    
    increment = int(10) 
    padding = int(1)
    
    if start == None:
        start = int(0)

    if id:
        id = int( float( id ) )
        posts = Guestbooks.active.filter(user_id=user.id, id__lt=id+1).order_by('-date_created')[start:int(start)+increment+padding]
    else:
        posts = Guestbooks.active.filter(user_id=user.id).order_by('-date_created')[start:int(start)+increment+padding]

    '''
    Notifications
    '''
    
    if request.user == user:
        notes = Notification.objects.filter(receiver=request.user, instance_type="Guestbooks")
        
        # Get hiligted
        hilight_numbers = []
        for note in notes:
            if note.status < 3:
                hilight_numbers.append( note.instance_id )
                
        # Get Unreplied posts
        unreplied_munber = []
        for note in notes:
            if note.status == 4:
                unreplied_munber.append( note.instance_id )
            
            
        # Set status on posts
        hilight_posts = []
        for post in posts:
            if post.id in hilight_numbers:
                post.hajlajt = True
                hilight_posts.append( post.id )
                post.unreplied = True
            
            if post.id in unreplied_munber:
                post.unreplied = True
                
        
        # Set status on hilightes to unreplied ( those we alredy have displayed )
        for note in notes:
            if note.instance_id in hilight_posts:
                note.status = 4
                note.save()

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
            
            try:
                unreplied_id = post_values['unreplied'] 
                unreplied = Notification.objects.get(receiver=request.user, instance_type="Guestbooks", instance_id=unreplied_id)
                unreplied.delete()
            except:
                pass
                
            guestbook = form.save()
        else:
            messages.add_message(request, messages.INFO, 'Nu blev det något fel')

    if request.is_ajax():
        return HttpResponse(status=200)
    else:
        template = "guestbook.html"

    return render(request, template, vars )
