# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from apps.core.utils import render
from models import Thread, ForumPost, defaultCategories
from forms import ThreadForm, ForumPostForm


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


@login_required(login_url='/auth/login/')
def create_thread(request):
    """
    Create a forum thread.
    
    """
    threads = Thread.active.all()
    form = ThreadForm()
    categories = defaultCategories.objects.all()
    
    if request.method == 'POST':    
        form = ThreadForm(request.POST)
        if form.is_valid():
            # Create the thread
            
            thread = Thread.objects.create(
                created_by = request.user,
                title = form.cleaned_data['title']
            )            
            
            tags = form.cleaned_data['tags']
            for tag in tags:
                thread.tags.add(tag.lower())

            # Create the initial post
            ForumPost.objects.create(
                created_by=request.user,
                collection=thread,
                body=form.cleaned_data['body']
            )
            return HttpResponseRedirect(thread.get_absolute_url())
    
    return render(request, 'create_thread.html', {"threads": threads, 'form': form, 'categories':categories})


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

    posts = ForumPost.objects.decorated(collection=thread)
    form = ForumPostForm()

    data = {"thread": thread, 'posts': posts, 'form': form, 'categories':categories}
    return render(request, 'thread.html', data)


@login_required(login_url='/auth/login/')
def create_forumpost(request):
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

@login_required(login_url='/auth/login/')
def get_threads_by_tags(request,tags):
    categories = defaultCategories.objects.all()
    tags = tags.split(",")
    threads = Thread.active.filter(tags__name__in=tags)
    
    if len( threads ) < 1:
        messages.add_message(request, messages.INFO, 'Hittade inga trådar =(')

    return render(request, 'forum.html', {"threads": threads,"categories":categories})
    