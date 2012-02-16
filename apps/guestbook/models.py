# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import get_model, Q
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher
from django.core.urlresolvers import reverse

from apps.core.signals import *

from apps.core.models import Entry

class Guestbooks(Entry):
    """
    A Post in the guestbook.

    """
    user_id = models.ForeignKey(User) 
    text = models.CharField(max_length=5120)

    def get_absolute_url(self):
        return "/user/{0}/guestbook/entry/{1}".format( self.user_id.id, self.id )
        
    def conversation(self):
        A = self.created_by
        B = self.user_id
        
        entrys_from_A_to_B = Q(created_by = A) & Q(user_id = B)
        entrys_from_B_to_A = Q(created_by = B) & Q(user_id = A)
        
        entrys = Guestbooks.active.filter(entrys_from_A_to_B | entrys_from_B_to_A)
        
        return entrys