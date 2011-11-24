from django.contrib.auth.models import User, Group
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from apps.core.utils import render
from models import Thread, ThreadHistory
from forms import ThreadForm

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
        Thread.objects.create(created_by=request.user, title=form.cleaned_data['title'])
    return render(request, 'forum.html', {"threads": threads, 'form': form})
