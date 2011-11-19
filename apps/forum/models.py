import datetime
from django.db import models
from django.db.models import get_model

from apps.core.models import ThreadedEntry, ThreadedEntryHistory, Entry, EntryHistory

class Thread(Entry):
    """
    A collection of ForumPost:s.

    """
    title = models.CharField(max_length=100)


class ThreadHistory(EntryHistory):
    """
    History for the Thread model.
    
    """
    title = models.CharField(max_length=100)


class ForumPost(ThreadedEntry):
    """
    A post in the forum.
    
    """
    collection = models.ForeignKey(Thread)
    body = models.TextField()


class ForumPostHistory(ThreadedEntryHistory):
    """
    History for the ForumPost model.
    
    """
    body = models.TextField()

