from models import Thread, ThreadHistory
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.contrib.auth.decorators import login_required

from apps.core.utils import render

def test_view(request):
    User.objects.all().delete()
    u = User.objects.create(username="aaaa")
    u2 = User.objects.create(username="aaaa2")
    t1 = Thread.objects.create(title="Thread 1")
    t1.title = "Thread 1 - Modified"
    t1.last_changed_by = u2
    t1.save()

    raise Http404

@login_required(login_url='/auth/login/')
def list_forum(request):
    results = " lol"
    return render(request,'forum.html', {"results": results})