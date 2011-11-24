from django.db import models
from django.db.models import get_model

from apps.core.models import Entry, EntryHistory

class Post(Entry):
    """
    A Post in the chat.

    """
    text = models.CharField(max_length=1024)