# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from apps.guestbook.models import Guestbooks

STATUS_CHOICES = (
    (0, u'Nytt'),
    (1, u'Nytt'),
    (2, u'Oläst'),
    (3, u'Obesvarat'),
)

NOTIFICATION_TYPES = (
    (1, 'Gästboksinlägg'),
    (2, 'Forumsvar'),
    (3, 'Artikelkommentar'),
    (4, 'Taggbevakning'),
)


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Notification(models.Model):
    
    # Datum skapad
    date_created = models.DateTimeField(auto_now_add = True, null=True)
    
    # Status för notifieringen
    status = models.IntegerField(choices=STATUS_CHOICES)
    
    # User that gets the notification
    receiver = models.ForeignKey(User, related_name="receiver_entries")

    # En relation till contentype, som möjligör generella relationer
    content_type = models.ForeignKey(ContentType)

    # ID för objektet som notifieringen berör
    object_id = models.PositiveIntegerField()

    # Content object
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    
    