# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from apps.core.models import Entry
    
class Article(Entry):
    """
    Articles

    """
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=5120)
    tags = TaggableManager()
    allow_comments = models.NullBooleanField(default=False)
    
    def get_absolute_url(self):
        return "/articles/read/%s/" % self.id
        
    def __unicode__(self):
        return u'%s' % self.title

class ArticleComment(MPTTModel):
    """ Threaded comments for blog posts """
    post = models.ForeignKey(Article)
    author = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, related_name="created_%(class)s_entries", blank=True, null=True)
    comment = models.TextField()
    added  = models.DateTimeField(default=datetime.datetime.now,blank=True)
    tags = TaggableManager()
    
    # a link to comment that is being replied, if one exists
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by=['added']
        
class defaultArticleCategories(models.Model):
    """
    Default categories for articles
    using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)
        

class ModeratorArticleCategories(models.Model):
    """
    Default categories for the articles
    for moderators, using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)