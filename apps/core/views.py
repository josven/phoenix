from core.models import Thread, ThreadHistory
from django.contrib.auth.models import User, Group
from django.http import Http404

def test_view(request):
    User.objects.all().delete()
    u = User.objects.create(username="aaaa")
    u2 = User.objects.create(username="aaaa2")
    t1 = Thread.objects.create(title="Thread 1")
    t1.title = "Thread 1 - Modified"
    t1.last_changed_by = u2
    t1.save()

    raise Http404
