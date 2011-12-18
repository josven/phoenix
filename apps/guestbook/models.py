from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User

from apps.core.models import Entry

class Guestbooks(Entry):
    """
    A Post in the guestbook.

    """
    user_id = models.ForeignKey(User) 
    text = models.CharField(max_length=5120)