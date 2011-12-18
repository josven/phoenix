import datetime
from django.db import models
from django.db.models import get_model
from taggit.managers import TaggableManager

from apps.core.models import ThreadedEntry, ThreadedEntryHistory, Entry, EntryHistory

class Thread(Entry):
    """
    A collection of ForumPost:s.

    """
    title = models.CharField(max_length=100)
    tags = TaggableManager()

    def get_absolute_url(self):
        return "/forum/thread/read/%s/" % self.id


class ThreadHistory(EntryHistory):
    """
    History for the Thread model.
    
    """
    origin = models.ForeignKey(Thread)
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
    origin = models.ForeignKey(ForumPost)
    body = models.TextField()


class defaultCategories(models.Model):
    """
    Default categories for the forum
    using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)
