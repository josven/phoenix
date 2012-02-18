# -*- coding: utf-8 -*-

import datetime
from django.db import models

from django.contrib.auth.models import User
from apps.guestbook.models import Guestbooks

STATUS_CHOICES = (
    (1, u'Nytt'),
    (2, u'Nytt'),
    (3, u'Obesvarat'),
    (4, u'Obesvarat'),
)

NOTIFICATION_TYPES = (
    (1, 'Gästboksinlägg'),
    (2, 'Forumsvar'),
    (3, 'Artikelkommentar'),
    (4, 'Taggbevakning'),
)

class Notification(models.Model):
    
    # Type of notification, mail, frindrequest ect
    type = models.CharField(max_length="1024")
    
    # Date created
    date_created = models.DateTimeField(auto_now_add = True, null=True)
    
    # Message, simple message that describes the notification
    message = models.CharField(max_length="1024")
    
    # If the user have seen the notification
    status = models.IntegerField(choices=STATUS_CHOICES)
    
    # User that gets the notification
    receiver = models.ForeignKey(User, related_name="receiver_entries")
    
    # If there is a user that sends
    sender = models.ForeignKey(User, related_name="sender_entries", blank=True, null=True)
    sender_name = models.CharField(max_length="1024", blank=True, null=True)
        
    # Instance info
    instance_type = models.CharField(max_length="1024")
    instance_id = models.IntegerField()
    instance_url = models.CharField(max_length="1024", blank=True, null=True)
    
    def __unicode__(self):        
        return NOTIFICATION_TYPES[ int( float( self.type ) ) - 1 ][1]
        
    def get_status(self):
        return STATUS_CHOICES[ int( float( self.status ) ) - 1 ][1]
    
    