# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from apps.notifications.models import *

NOTIFICATION_TYPES = (
    (1, 'Gästboksinlägg'),
)

@never_cache
@login_required(login_url='/auth/login/')
def updates(request, format):
    
    if request.is_ajax():
        
        data = get_notifications(request.user)
        
        if format == 'xml':
            mimetype = 'application/xml; charset=utf8'
            
        if format == 'json':
            mimetype = 'application/javascript; charset=utf8'
        
        json_data = simplejson.dumps( data )
 
        return HttpResponse(json_data,mimetype)
   
    else:
    
        return HttpResponse(status=400)       
    
    
def get_notifications(user):
    
    d = {}

    notifications = Notification.objects.filter(receiver=user)
    
    if notifications:

        count_new_guestbook = 0
        count_indicator_guestbook = 0
        
        for notification in notifications:
        
            # Get new guestbook annuoucements
            if ( notification.instance_type == "Guestbooks" ) & ( int( float( notification.status ) ) == 1 ):
                count_new_guestbook += 1
                notification.status = 2
                notification.save()
            
            # Get guestbook indicator       
            if ( notification.instance_type == "Guestbooks" ) & ( int( float( notification.status ) ) < 4 ):
                count_indicator_guestbook += 1
        
        d = { 'a' : { 'gb' : count_new_guestbook }, 'i' : { 'gb' : count_indicator_guestbook } }
     
    return d

    
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




