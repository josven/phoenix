from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from apps.core.utils import render
from models import Thread, ForumPost
from forms import ThreadForm, ForumPostForm


@login_required(login_url='/auth/login/')
def read_forum(request):
    """
    Read the list of forum threads.
    
    """
    threads = Thread.active.all()
    form = ThreadForm()
    return render(request, 'forum.html', {"threads": threads, 'form': form})


@login_required(login_url='/auth/login/')
def create_thread(request):
    """
    Create a forum thread.
    
    """
    threads = Thread.active.all()
    form = ThreadForm(request.POST)
    if form.is_valid():
        # Create the thread
        thread = Thread.objects.create(
            created_by=request.user,
            title=form.cleaned_data['title']
        )

        # Create the initial post
        ForumPost.objects.create(
            created_by=request.user,
            collection=thread,
            body=form.cleaned_data['body']
        )
        return HttpResponseRedirect(thread.get_absolute_url())
    return render(request, 'forum.html', {"threads": threads, 'form': form})


@login_required(login_url='/auth/login/')
def read_thread(request, id):
    """
    Read a forum thread.
    
    """
    try:
        thread = Thread.active.get(id=id)
    except:
        raise Http404

    posts = ForumPost.objects.decorated(collection=thread)
    form = ForumPostForm()

    data = {"thread": thread, 'posts': posts, 'form': form}
    return render(request, 'thread.html', data)


@login_required(login_url='/auth/login/')
def create_forumpost(request):
    """
    Create a forumpost. FormPost class will handle all threading logic.
    
    """
    form = ForumPostForm(request.POST)
    if form.is_valid():
        try:
            thread = Thread.active.get(id=thread_id)
        except:
            raise Http404

        # If the parent does not equal the given thread, abort!
        if parent_id in form.cleaned_data:
            try:
                parent = ForumPost.objects.get()
            except:
                raise Http404
            if parent.collection != thread:
                raise Hell

        # Create the post
        ForumPost.objects.create(
            created_by=request.user,
            parent_id=parent_id,
            collection=thread
        )

        return aasd
