# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect  
from django.utils.encoding import force_unicode

from apps.notifications.models import *
from apps.core.utils import render

NOTIFICATION_TYPES = (
    (1, 'Gästboksinlägg'),
    (2, 'Forumsvar'),
    (3, 'Artikelkommentar'),
    (4, 'Taggbevakning'),
)

@never_cache
@login_required()
def delete_notification(request):
    if request.method == 'POST':
        
        notification_ids = map(int, request.POST.getlist('notification'))
        model = request.POST.get('model')
        notifications = request.user.receiver_entries.filter(id__in = notification_ids)
        
        for note in notifications:
            note.delete()

        return HttpResponse(status=200)

    return HttpResponseRedirect(request.META["HTTP_REFERER"]) 

@never_cache
@login_required()
def updates(request, format):
    
    data = {}

    if True: #not request.is_ajax():
        if request.user.is_authenticated():

            # Ta upp notificationer som ska annonseras
            if request.GET.get('n', None):
                
                notifications = request.user.receiver_entries.filter( status__in = [0,1] )
                notification_count = len( notifications )

                announced_notifications = [ note for note in notifications if note.status in [0]]
                announced_notifications_length = len( announced_notifications )

                new_notifications = [ note for note in notifications if note.status in [1]]
                new_notifications_length = len( new_notifications )

                if announced_notifications:
                    
                    announced_notifications_length = len( announced_notifications )
                    
                    if announced_notifications_length == 1:
                        
                        note = announced_notifications[0]

                        message = u'Ny aktivitet!<br/> {0} </br> <a href="{1}">Gå dit</a>'.format( force_unicode(note.content_object.get_verbose_name), force_unicode( note.content_object.get_absolute_url() ) )
                    
                    if announced_notifications_length > 1:
                        
                        message = u'{0} nya aktiviteter!<br/> <a href="{1}">Gå dit</a>'.format( announced_notifications_length , reverse('read_notifications') )

                    data['notification_message'] = message
                
                data['notification_count'] = notification_count
                for a_note in announced_notifications:
                    a_note.status = 1
                    a_note.save()

        json_data = simplejson.dumps( data )

        return HttpResponse(json_data, content_type='application/json; charset=UTF-8')
   
    else:

        return HttpResponse(status=400)       
    

def get_notifications(request):
    
    d = {}
    '''
    user = request.user
    
    notifications = Notification.objects.filter(receiver=user)
    
    
    #Tests
    testdict = {}
    for note in notifications.values():
        testdict[ note['instance_type'] ] = {}
        testdict[ note['instance_type'] ][ note['status'] ] = {}
        testdict[ note['instance_type'] ][ note['status'] ][ note['instance_id'] ] = note
    
    count_new_guestbook = 0
    count_indicator_guestbook = 0

    count_new_forum = 0
    count_indicator_forum = 0

    count_new_article = 0
    count_indicator_article = 0
        
    if notifications:
        
        for notification in notifications:
        
            # Get new guestbook annuoucements
            if ( notification.instance_type == "Guestbooks" ) & ( int( float( notification.status ) ) == 1 ):
                count_new_guestbook += 1
                notification.status = 2
                notification.save()
            
            # Get guestbook indicator       
            if ( notification.instance_type == "Guestbooks" ) & ( int( float( notification.status ) ) < 3 ):
                count_indicator_guestbook += 1    
                
            # Get new forum annuoucements            
            if ( notification.instance_type == 'ForumComment' ) & ( int( float( notification.status ) ) == 1 ):
                count_new_forum += 1
                notification.status = 2
                notification.save()
            
            # Get forum indicator       
            if ( notification.instance_type == 'ForumComment' ) & ( int( float( notification.status ) ) < 3 ):
                count_indicator_forum += 1  
                              
            # Get new article annuoucements            
            if ( notification.instance_type == 'ArticleComment' ) & ( int( float( notification.status ) ) == 1 ):
                count_new_article += 1
                notification.status = 2
                notification.save()
            
            # Get articlecomment indicator       
            if ( notification.instance_type == 'ArticleComment' ) & ( int( float( notification.status ) ) < 3 ):
                count_indicator_article += 1
        
    d = {
        'notifications':notifications,
        'test':testdict,
        'a' : { 'gb' : count_new_guestbook, 'fo' : count_new_forum , 'ar' : count_new_article },
        'i' : { 'gb' : count_indicator_guestbook, 'fo' : count_indicator_forum, 'ar' : count_indicator_article } 
        }
    '''
    return d

    
@never_cache
@login_required()
def notifications(request):
    vars = {
            'notifications' : request.user.receiver_entries.all(),
        }

    
    return render(request, "notifications.html", vars )
    
    
'''
        for status in STATUS_CHOICES:
            
            
            
            for type in NOTIFICATION_TYPES:
                
                
                for notification in notifications:
                        
                        #print d['a'][ 't' ][ str( type[0] ) ][ str( status[0] ) ]['amount'] += 1
                        
                        
                        # Announcemets
                        
                        if notification.status == 1:
                            #updates_dict['a'][ str( status ) ][ str( type )]['text'] = "nonsens"
                            d['a'][ 't' ][ str( type[0] ) ][ str( status[0] ) ]['amount'] += 1
                        
                        
                        
                        # Indicators
                        if notification.status < 4:
                            updates_dict['i'][ str( status ) ][ str( type )]['text'] = "nonsen igen"
                            d['i'][ 't' ][ str( type[0] ) ][ str( status[0] ) ]['amount'] += 1


            for type in NOTIFICATION_TYPES:
                
                type_dict = {}
                
                
                for notification in notifications:
                    
                    
                    
                    # Only annonce new notification
                    if notification.status == 1: #NEW
                        
                        if int( float( notification.type[0] ) ) == int( float ( type[0] ) ):                              
                            print "New {0} status {1}".format( notification.type, notification.status )
                            
                            type_dict[ str( type[0] ) ]['a'].append( notification )

                            # Set status on the notification to annonced
                            notification.status = 2
                            notification.save()
                    
                    # alert noteicationns, used for counters in the menubar
                    if notification.status < 4: #All notifications exect for unreplied
                        
                        if int( float( notification.type[0] ) ) == int( float ( type[0] ) ):  
                            print "Status alert: {0} status {1}".format( notification.type, notification.status )
                            
                            
                    
                amount_of_messages =  len( typearray )
                
                # if only one note of that type
                if amount_of_messages == 1:
                    messages_dict[str (type[0])] = {'number': 1, 'text': notification.message}
                        
                # If more then one note in that type, collect them in one message
                elif amount_of_messages > 1:
                    messages_dict[str (type[0])] = {'number': amount_of_messages, 'text': "Nytt! {0} {1}".format( amount_of_messages, type[1] )}
                
    #return "TEST"
        
'''




