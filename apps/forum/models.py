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
    posts_index = models.IntegerField(null=True, blank=True)
    last_post = models.ForeignKey('ForumPost', null=True, blank=True, default = None)
    
    def get_absolute_url(self):
        return "/forum/thread/read/%s/" % self.id
    
    def __unicode__(self):
        return u'%s' % self.title

    def get_latest_post(self):
        if not self.last_post:
            self.last_post = ForumPost.objects.filter(collection=self).order_by('-id')[0]
        return self.last_post

    def get_number_of_post(self):
        
        if not self.posts_index:
            number = len ( ForumPost.objects.decorated(collection=self) )
            self.posts_index = number
        
        number = self.posts_index -1
        
        if number < 0:
            number = 0
            
        return number

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
    
    def __unicode__(self):
    
        text = u"Forumpost #{0} av {1}. {2}...".format(self.id, self.created_by, self.body[:10])
        
        return text


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
