# -*- coding: utf-8 -*-
from django.core import serializers
from django.contrib import messages
from apps.notifications.models import *
from apps.notifications.views import get_notifications
 
NOTIFICATION_TYPES = (
    (1, 'Gästboksinlägg'),
)

class AnnonuceNotifications(object):
    def process_request(self, request):
        if not request.is_ajax():
            if request.user.is_authenticated():
                data = get_notifications(request.user)
        
                # Annonce guestbook notifications
                guestbook_announcements = data['a']['gb']
                if guestbook_announcements == 1:
                    messages.add_message(request, messages.INFO, "Nytt gästboksinlägg")
                
                if guestbook_announcements > 1:
                    messages.add_message(request, messages.INFO, "{0} nya gästboksinlägg".format( guestbook_announcements ) )

                # Put indicators on 
                request.__class__.indicators = data['i']




    '''
    def process_request(self, request):
        """
        Notification
    
        """
        if request.user.is_authenticated():
            notifications = Notification.objects.filter(receiver=request.user)
            
            if notifications:
                
                # Array that hols all the messages that we sen via django.contrib.messages
                messages_array = []
            
                for type in NOTIFICATION_TYPES:
                    
                    typearray = []
                    
                    for notification in notifications:
                         
                        # Only annonce new notification
                        if notification.status == 1: #NEW
                            
                            if int( float( notification.type[0] ) ) == int( float ( type[0] ) ):                              
                                print "New {0} status {1}".format( notification.type, notification.status )
                                
                                typearray.append( notification )

                                # Set status on the notification to annonced
                                notification.status = 2
                                notification.save()
                                
                    amount_of_messages =  len( typearray )
                    print "amount_of_messages : {0} in {1}".format( amount_of_messages, type[0] )
                            
                    # if only one note of that type
                    if amount_of_messages == 1:
                        messages_array.append( "{0}".format(notification.message) );
                            
                    # If more then one note in that type, collect them in one message
                    elif amount_of_messages > 1:
                        messages_array.append( "Nytt! {0} {1}".format( amount_of_messages, type[1] ) );
              
                for message in messages_array:
                    messages.add_message(request, messages.INFO, message)
    '''
