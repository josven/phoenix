# -*- coding: utf-8 -*-
from django.core import serializers
from django.contrib import messages
from apps.notifications.models import *

class AnnonuceNotifications(object):

    def process_request(self, request):
        """
        Notification
    
        """
        
        if request.user.is_authenticated():
            notifications = Notification.objects.filter(receiver=request.user)
            #notification_json = serializers.serialize('json', [ notifications, ])
     
            if notifications:
                for notification in notifications:
                    if notification.status == 1: #NEW
                        Message = u"Ny händelse! {0}".format(notification.message);
                        messages.add_message(request, messages.INFO, Message)
                        notification.status = 2
                        notification.save()
                    
                    
     
    
        '''
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip
        '''