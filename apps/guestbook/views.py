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
def guestbook_conversation(request,sender_id,reciver_id):
    
    A = int( float (sender_id) )
    B = int( float (reciver_id) )
    
    vars = {
            'form' : GuestbookForm(),
            }

    users = [A, B]
    kompis = None
    
    for user in users:        
        if user != request.user.id:
            kompis = User.objects.get(id=user)

    # if user can see the converstion
    if request.user.id in users:
    
        entrys_from_A_to_B = Q(created_by__id = A) & Q(user_id__id = B)
        entrys_from_B_to_A = Q(created_by__id = B) & Q(user_id__id = A)
        
        vars['entries'] = Guestbooks.active.filter(entrys_from_A_to_B | entrys_from_B_to_A).order_by('-date_created')
        
        vars['page_title'] = u'Gästbokskonversation mellan dig och {0}'.format(kompis) 
    
        if request.method == 'POST':
            _post_guestbook(request, kompis.id)
        
        return render(request, "guestbook.html", vars )
        
    return HttpResponse(status=401)
    

@never_cache
@login_required(login_url='/auth/login/')
def guestbook(request,userid):
    """
    Guestbook
    
    """

    user = User.objects.get(pk=userid)
    entries = Guestbooks.active.filter(user_id=user.id).order_by('-date_created')
    vars = {
            'form' : GuestbookForm(),
            'entries' : entries,
            'profile' : user.get_profile(),
            }
    
    if request.user.id == int( float( userid ) ):
        vars['page_title'] = u'Din egen gästbok'
    else:
        vars['page_title'] = u'{0} gästbok'.format(user)

    if request.method == 'POST':
        _post_guestbook(request, userid)


    if request.is_ajax():
        return HttpResponse(status=200)
    else:
        template = "guestbook.html"

    return render(request, template, vars )

def _post_guestbook(request,userid):
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