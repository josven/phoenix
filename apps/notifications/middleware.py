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
                data = get_notifications(request)
        
                #Get annoncements
                annoncements = data.get('a', None)
                if annoncements:
                    
                    # Get guestbook annoncements
                    guestbook_annoncements = annoncements.get('gb', None)
                    if guestbook_annoncements:
                        
                        if guestbook_annoncements == 1:
                            messages.add_message(request, messages.INFO, "Nytt gästboksinlägg")
                        
                        if guestbook_annoncements > 1:
                            messages.add_message(request, messages.INFO, "{0} nya gästboksinlägg".format( guestbook_annoncements ) )
                        
                    # Get forum annoncements
                    forum_annoncements = annoncements.get('fo', None)
                    if forum_annoncements:
                        
                        if forum_annoncements == 1:
                            messages.add_message(request, messages.INFO, "Nytt svar i forumet")
                        
                        if forum_annoncements > 1:
                            messages.add_message(request, messages.INFO, "{0} nya svar i forumet".format( forum_annoncements ) )
                   
                                                             
                # Put indicators on 
                request.__class__.indicators = data.get('i',None)
