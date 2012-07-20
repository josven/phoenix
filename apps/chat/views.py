# -*- coding: utf-8 -*-

from models import *
from forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

import site_settings

from apps.core.utils import render

@login_required()
def camchat(request):
    """
    Temporary chamchat
    
    """

    vars = {
        'app_name':'camchat'
        }
    messages.add_message(request, messages.INFO, 'Lösenord är:fisk')    
    return render(request,'tinychat.html', vars)

@never_cache
@login_required()
def chat(request):
    """
    Chat view, render chat page
    
    """
    vars = {
        'form' : PostForm(),
        'comments' : Post.active.order_by('-date_created').select_related('created_by','created_by__profile__photo').order_by('-id')[:site_settings.CHAT_LIST_ITEM_LIMIT]
    }
    
    return render(request,'chat.html', vars)

@login_required()
def post_chat(request):
    """
    Chat post, only ajax
    
    """
    if request.is_ajax():
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                if len( form.clean()['text'] ) > 4:
                    form.save()
                    return HttpResponse(status=200) # OK!
                    
            # Change to a more appropite statuscode?
            return HttpResponse(status=404) 
    
    # Only allow ajax post
    return HttpResponse(status=404)

@never_cache   
@login_required()
def get_chat(request):
    """
    Chat get, only ajax
    
    """
    
    vars = {}
    
    if request.is_ajax():     
        if request.method == 'GET':
            
            posts = Post.active.order_by('-date_created')[:site_settings.CHAT_LIST_ITEM_LIMIT]
            client_post = int(float( request.GET.get('s', '0') ) )
            current_post = int(float( posts[0].id ) )
            number_of_posts = current_post - client_post
            
            if number_of_posts != 0:
                vars['posts'] = posts[0:number_of_posts]
                return render(request,'_chat.html', vars)
                
            return HttpResponse(status=302) # Not changed
    
    # Only allow ajax get
    return HttpResponse(status=404)