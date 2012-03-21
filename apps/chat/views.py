import json 
from models import *
from forms import *
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.http import Http404, HttpResponse
from django.conf import settings

import site_settings

from apps.core.utils import render

"""
    TO DO
    - Move constants to a seperate settings file.
    - read_post()
    - delete_post()
    - Use (CURD) in chat(request, **kwargs) depending on POST GET UPDATE and DELETE

"""

@never_cache
@login_required(login_url='/auth/login/')
def camchat(request):
    vars = {
        'app_name':'camchat'
        }
    messages.add_message(request, messages.INFO, 'Lösenord är:fisk')    
    return render(request,'tinychat.html', vars)
    

@login_required(login_url='/auth/login/')
def chat(request):
    vars = {
        "isFirstPage":True
    }
    
    if request.is_ajax():
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                if len( form.clean()['text'] ) > 4:
                    form.save()
                    return HttpResponse(status=200) # OK!
            return HttpResponse(status=404) #CHANGE THIS

    vars['form'] = PostForm()
    vars['posts'] = Post.active.order_by('-date_created')[:site_settings.CHAT_LIST_ITEM_LIMIT]

    return render(request,'chat.html', vars)

@never_cache   
@login_required(login_url='/auth/login/')
def get_chat(request):
    
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
    

'''
OLD

@never_cache
@login_required(login_url='/auth/login/')
def chatpost(request,id,type):
    """
    
    API for GET posts in HTML
    Later this will also return 
    json and xml depending on <type>
    
    """
    try:
        post = Post.objects.get(id=id)
    except:
        # "no match"
        raise Http404  
    
    if request.method == 'GET':
        if type == 'html':
            form = PostForm()
            posts = [post]
            return render(request,'chat.html', {"posts":posts,"form":form})
        else:
            # "wrong format"
            raise Http404
    else:
        # "wrong method"
        raise Http404

@never_cache
@login_required(login_url='/auth/login/')
def chatposts(request,id1,id2,type):
    """
    
    API for GET a range of posts in HTML
    
    """
    
    vars = {
        'isFirstPage': False,
        'isLastPage': False,
        }
    
    # Check order
    if int(id1) > int(id2):
        # "reverse"
        start = int(id2)
        stop = int(id1)
    else:
        # " not reverse"
        start = int(id1)
        stop = int(id2)
    
    # Check if theres a negative value or its the first page
    if start <= 1:
        # "First page"
        vars['isLastPage'] = True
        start = 1
    
    try:
        # Add +1 padding to deteminate if its any more posts
        posts = Post.objects.filter(id__range=(start,stop+1)).order_by('-date_created')
        
        # Control if its the last page
        if posts[0].id <= stop:
            vars['isFirstPage'] = True
        else:
           # Trim query to match orginal request
           posts = posts[1:site_settings.CHAT_LIST_ITEM_LIMIT+1]
    except:
        # "no match"
        raise Http404
    
    if request.method == 'GET':
        if type == 'html':
            form = PostForm()
            vars['posts'] = posts
            vars['form'] = form
            return render(request,'chat.html', vars)
        else:
            #"wrong format"
            raise Http404
    else:
        # "wrong method"
        raise Http404
'''
