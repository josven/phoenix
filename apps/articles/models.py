# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

import datetime

from apps.core.models import Entry

from apps.core.signals import *

class Article(Entry):
    """
    Articles

    """
    title = models.CharField(max_length=128, verbose_name="Rubrik")
    body = models.TextField(max_length=5120, verbose_name="Text")
    tags = TaggableManager(verbose_name="Kategorier")
    allow_comments = models.NullBooleanField(default=False,verbose_name="Tillåt kommentarer")
        
    @property
    def ajax_editable_fields(self):
        return ["body", "allow_comments"]

    @property
    def is_deleteble(self):
        return True
        
    @property
    def delete_next_url(self):
        return reverse('read_article')
        
    @property
    def is_editable(self):
        """
        Limit is_editable to one day
        """
        return datetime.datetime.now() - self.date_created < datetime.timedelta(days=1)
           
    @property
    def allow_history(self):
        return True    
        
    @property
    def fields_history(self):
        return ["body"]

    def get_absolute_url(self):
        return "/articles/read/%s/" % self.id
        
    def __unicode__(self):
        return u'%s' % self.title

    def aaData(self):
        """
        aaData formats for datatables
        """

        title = u"<a href=\"{0}\" >{1}</a>".format( self.get_absolute_url(), self.title )
        tags = [u"<span class=\"ui-tag\"><a href=\"{0}\">{1}</a></span>".format( reverse( 'search_article', args = [ tag.name ]), unicode(tag.name).title()  ) for tag in self.tags.all()]
        created = u"{0} {1} av <a href=\"{2}\">{3}</a>".format(naturalday(self.date_created), self.date_created.strftime("%H:%M"), self.created_by.get_profile().get_absolute_url(), self.created_by.username)
        
        if self.allow_comments:
            allow_comments = self.get_posts_index()
        else:
            allow_comments = "-"

        data =  {
                'title': title,
                'created': created,
                'tags' : u" ".join( tags ),
                'allow_comments': allow_comments,
                'id': self.id,
                }
           
        return data
    
    def get_posts_index(self):   
        return ArticleComment.objects.filter(post=self).count()
        
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

    def get_absolute_url(self):
        return "/articles/read/{0}/#comment-{1}".format( self.post.id, self.id )
        
    @property
    def get_reply_url(self):
        return reverse('comment_article', args=[self.post.id])

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
        
        
        
