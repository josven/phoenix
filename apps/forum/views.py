# -*- coding: utf-8 -*-
import re
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from apps.core.utils import render, validate_internal_tags
from models import Thread, ForumPost, defaultCategories
from forms import *

@never_cache
@login_required(login_url='/auth/login/')
def read_forum(request):
    """
    Read the list of forum threads.
    
    """

    categories = defaultCategories.objects.all()
    threads = Thread.active.all()
  
    vars = {
            "threads": threads,
            "categories":categories
            }

    return render(request, 'forum.html', vars )

@never_cache
@login_required(login_url='/auth/login/')
def create_thread(request, tags=None):
    """
    Create a forum thread.
    
    """

    threads = Thread.active.all()
    form = ThreadForm()
    tagform = DefaultForumTagsForm()
    categories = defaultCategories.objects.all()
    
    if tags != None:
        initial_tags = tags.split(',')
        tagform = DefaultForumTagsForm(initial={'default_tags': initial_tags })
    
    if request.method == 'POST':    
        form = ThreadForm(request.POST)
        tagform = DefaultForumTagsForm(request.POST)
        
        if form.is_valid() & tagform.is_valid():            
            default_tags = tagform.cleaned_data['default_tags']
            user_tags = form.cleaned_data['tags']
            
            # Clean tags from non alphanumeric chars
            cleaned_tags = list( re.sub(r'\W', ' ', tag).strip() for tag in user_tags) 
                
            # Filter list from empty strings
            cleaned_tags = filter(None, cleaned_tags)
            
            # Combine and remove doubles
            all_tags = list(set(default_tags + cleaned_tags))
                
            # Check if a default tag is present
            if len(default_tags) == 0:
                messages.add_message(request, messages.INFO, 'Du måste välja minst en huvudkategori!')
                return render(request, 'create_thread.html', {"threads": threads, 'form': form,'tagform':tagform, 'categories':categories})

            # Check maximum allowed tags
            if len( all_tags ) > 5:
                messages.add_message(request, messages.INFO, 'Du kan inte välja fler än fem kategorier!')
                return render(request, 'create_thread.html', {"threads": threads, 'form': form,'tagform':tagform, 'categories':categories})

            # Validate INTERNAL tags
            all_tags = validate_internal_tags(request, all_tags) 
            
            print all_tags
            # Create the thread
            thread = Thread.objects.create(
                created_by = request.user,
                title = form.cleaned_data['title']
            ) 
            
            # Apply tags on thread
            for tag in all_tags:
                thread.tags.add(tag)  
            
            # Create the initial post
            ForumPost.objects.create(
                created_by=request.user,
                collection=thread,
                body=form.cleaned_data['body']
            )
            
            return HttpResponseRedirect(thread.get_absolute_url())

    return render(request, 'create_thread.html', {"threads": threads, 'form': form,'tagform':tagform, 'categories':categories})

@never_cache
@login_required(login_url='/auth/login/')
def read_thread(request, id):
    """
    Read a forum thread.
    
    """
    categories = defaultCategories.objects.all()
    
    try:
        thread = Thread.active.get(id=id)
    except:
        raise Http404

    posts = ForumPost.objects.decorated(collection=thread, deleted_by=None)
    
    form = ForumPostForm()

    data = {"thread": thread, 'posts': posts, 'form': form, 'categories':categories}
    return render(request, 'thread.html', data)

@never_cache
@login_required(login_url='/auth/login/')
def create_forumpost(request, tags=None):
    """
    Create a forumpost. FormPost class will handle all threading logic.
    
    """
    form = ForumPostForm(request.POST)
    if form.is_valid():
        try:
            thread = Thread.active.get(id=form.cleaned_data['thread_id'])
        except:
            raise Http404

        # If the parent does not equal the given thread, abort!
        if 'parent_id' in form.cleaned_data and form.cleaned_data['parent_id']:
            try:
                parent = ForumPost.objects.get(id=form.cleaned_data['parent_id'])
            except:
                raise Http404
            if parent.collection != thread:
                raise Http404

        # Create the post
        ForumPost.objects.create(
            parent_id=form.cleaned_data['parent_id'],
            created_by=request.user,
            collection=thread,
            body=form.cleaned_data['body']
        )
        return HttpResponseRedirect(thread.get_absolute_url())

    try:
        thread = Thread.active.get(id=request.POST['thread_id'])
    except:
        raise Http404
    posts = ForumPost.objects.decorated(collection=thread)
    form = ForumPostForm()

    data = {"thread": thread, 'posts': posts, 'form': form}
    return render(request, 'thread.html', data)

@never_cache
@login_required(login_url='/auth/login/')
def get_threads_by_tags(request,tags):
    categories = defaultCategories.objects.all()
    tags_array = tags.split(",")
    threads = Thread.active.filter(tags__name__in=tags_array)
    
    if len( threads ) < 1:
        messages.add_message(request, messages.INFO, 'Hittade inga trådar =(')

    return render(request, 'forum.html', {"threads": threads,"categories":categories,"tags":tags})
    