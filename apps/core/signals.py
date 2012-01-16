# -*- coding: utf-8 -*-
import datetime

from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core import serializers
from django.core.signals import request_finished
from django.dispatch import receiver

from apps.notifications.models import *

#from apps.articles.models import Article
from apps.guestbook.models import Guestbooks


@receiver(post_save, sender=Guestbooks)
def guestbook_reciver(sender, **kwargs):
    print "SIGNAL!"
    instance = kwargs['instance']

    notification = Notification(
        type = "Gästboksinlägg",
        message = 'Nytt gästboksinlägg!',
        status = 1, #NEW
        receiver = instance.user_id,
        sender = instance.created_by,
        sender_name = instance.created_by.username,
        instance_type = instance.__class__.__name__,
        instance_id = instance.id,
        instance_url = instance.get_absolute_url(),
        ).save()
    
    
'''    
def _all_unexpired_sessions_for_user(user):
    user_sessions = []
    all_sessions  = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    for session in all_sessions:
        session_data = session.get_decoded()
        if user.pk == session_data.get('_auth_user_id'):
            user_sessions.append(session.pk)
    return Session.objects.filter(pk__in=user_sessions)
    
    
def _set_notification(notification):
    
    # prepare notification to json
    notification_json = serializers.serialize('json', [ notification, ])
    
    # Get receiver
    receiver = User.objects.get(id=notification.receiver_id)
    
    if receiver.is_authenticated():
        
        sessions = _all_unexpired_sessions_for_user(receiver)
        notify_array = []
        
        for session in sessions:
        
            decoded = session.get_decoded().get('notifications',None)
            
            if type(decoded) is list:
                
                note = decoded
                
                if note:
                    notify_array.extend(note)

        
        # TODO reduce array  get rid of dubbules
        
        # store new note in array
        print "START!"
        print notify_array
        #notify_array.extend(notification_json)
        notify_array.extend([notification_json])
        print notify_array
        print "END!"
        
        #store array in sessions.
        for session in sessions:
            session_decoded = session.get_decoded()
            session_decoded['notifications'] = notify_array
            session.session_data = Session.objects.encode(session_decoded)
            session.save() 
            
        #test
        test_sessions = _all_unexpired_sessions_for_user(receiver)
        for test_session in test_sessions:
            test_session_decoded = test_session.get_decoded()
            notes = test_session_decoded.get('notifications',None)
            
            for note in notes:
                print "################# NOTE ########"
                print note
                
            #print test_session_decoded
            #print "########### TEST SESSION DATA #############"
            #print test_session_decoded.get('notifications',None)
        

    
   
    if session is active:
        
        get all un expired sessions

        notify_array = []
        
        for session in sessions:
            put notifies in array
        
        store new notify in array
        reduce array # get rid of dubbules
        
        store array in _current_ session.
         
    else
        save instance
        


    

@receiver(user_logged_out)
def log_logout(sender, **kwargs):
    u = kwargs['user'].username 
    data={ 'Successful Logout': u } 
    
    session = kwargs['request'].session
    session['testlol'] = "sparat"    
    
    data={ 'Successful Logout': u }
    
    #transaction.add(data)
    print data
    
    
@receiver(user_logged_in)
def log_login(sender, **kwargs):
    u = kwargs['user'] 
    
    
    sessions = _all_unexpired_sessions_for_user(u)
    print sessions
    
    #print session.get('testlol',None)
    
    data={ 'Successful Login': u.username }
    #transaction.add(data)
    print data
    
    
def _all_unexpired_sessions_for_user(user):
    user_sessions = []
    all_sessions  = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    for session in all_sessions:
        session_data = session.get_decoded()
        if user.pk == session_data.get('_auth_user_id'):
            user_sessions.append(session.pk)
    return Session.objects.filter(pk__in=user_sessions)
'''