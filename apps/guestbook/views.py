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
@login_required()
def guestbook_conversation(request,sender_id,reciver_id, id=None):

    A = int( float (sender_id) )
    B = int( float (reciver_id) )

    users = [A, B]
    kompis = None
    
    for user in users:        
        if user != request.user.id:
            kompis = User.objects.get(id=user)

    vars = {
            'form' : GuestbookForm(initial={'user_id': kompis.id}),
            'temple_type': "conversation",
            }

    # if user can see the converstion
    if request.user.id in users:
    
        entrys_from_A_to_B = Q(created_by__id = A) & Q(user_id__id = B)
        entrys_from_B_to_A = Q(created_by__id = B) & Q(user_id__id = A)
        
        vars['entries'] = Guestbooks.active.filter(entrys_from_A_to_B | entrys_from_B_to_A).order_by('-date_created')
        
        vars['page_title'] = u'Gästbokskonversation mellan {0} och {1}'.format(request.user.username, kompis) 
        vars['users'] = users
    
        if request.method == 'POST':
            form = GuestbookForm( request.POST )
            
            if form.is_valid():
                form.save()
                
                # Tar bara upp notifikationer som tillhör inlägget man svarar på
                if id:
                    notifications = request.user.receiver_entries.filter(content_type__model = 'guestbooks', object_id__in = [id])
                    for note in notifications:
                        note.delete()

                if request.is_ajax():
                    return render(request, "_guestbook_comments.html", vars )

        return render(request, "guestbook.html", vars )
        
    return HttpResponse(status=401)
    

@never_cache
@login_required()
def guestbook(request,userid):
    """
    Guestbook
    
    """

    user = User.objects.get(pk=userid)
    entries = Guestbooks.active.filter(user_id=user.id).order_by('-date_created')
    vars = {
            'form' : GuestbookForm(initial={'user_id': userid}),
            'entries' : entries,
            'profile' : user.get_profile(),
            'user' : user,
            'page_title' : u'Gästbok för {0}'.format(user.username),
            }

    if request.method == 'POST':
        form = GuestbookForm( request.POST )
        
        if form.is_valid():
            form.save()
            
            if request.is_ajax():
                return render(request, "_guestbook_comments.html", vars )

    return render(request, "guestbook.html", vars )

@never_cache
@login_required()
def guestbook_entry_delete(request, userid, id):
    if request.is_ajax():



        vars = {
            'form' : DeleteGuestbookForm(),
            'user' : User.objects.get(pk=userid),
            'entry' : Guestbooks.active.get(id=id),
            }

        this_user = request.user
        guestbook_owner = vars['user']
        entry_owner = vars['entry'].created_by

        # Kollar så att man får ta bort inlägget
        if this_user == guestbook_owner or this_user == entry_owner:

            # Returnera ett delete formulär
            if request.method == 'GET':
                vars['form'] = DeleteGuestbookForm( instance = vars['entry'] )
                return render(request, "guestbook_delete.html", vars )

            # Ta bort inlägget
            if request.method == 'POST':
                vars['form'] = DeleteGuestbookForm( request.POST, instance = vars['entry'])

                if vars['form'].is_valid():
                    entry = vars['form'].save(commit=False)
                    entry.delete()
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=428)

    return HttpResponse(status=401)

@never_cache
@login_required()
def guestbook_entry(request, userid, id=None):
    
    print "guestbook_entry"
    # userid = ägaren för gästboken, vanligtvis alltid reuqest.user som svarar
    # id = gästboksinlägget som man svarar på, detta för att ta bort ev notifikationer
    
    user = User.objects.get(pk=userid)
    
    vars = {
        'form' : GuestbookForm(request.POST or None),
        'profile' : user.get_profile(),
        'user' : user,
        'page_title' : u'Gästbok för {0}'.format(user.username),
        }

    # Svara på ett gästbooksinlägg
    if request.method == 'POST':

        if vars['form'].is_valid():
            new_entry = vars['form'].save()

            # Om det är ens egen gästbok
            if request.user.id == int( float( userid ) ):

                # Tar bara upp notifikationer som tillhör inlägget man svarar på
                if id:
                    notifications = request.user.receiver_entries.filter(content_type__model = 'guestbooks', object_id__in = [id])
                    for note in notifications:
                        note.delete()
        

        vars['entries'] = Guestbooks.active.filter(user_id=user.id).order_by('-date_created')

        if request.is_ajax():
            return render(request, "_guestbook_comments.html", vars )
        return render(request, "guestbook.html", vars )

    # Visar ett inlägg
    if request.method == 'GET':
        
        vars['entries'] = Guestbooks.active.filter(id = id)
        return render(request, "guestbook.html", vars )

    # If evertything else fails
    return HttpResponse(status=404)