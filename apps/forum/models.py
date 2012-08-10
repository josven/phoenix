# -*- coding: utf-8 -*-

import datetime
import time

from urllib import quote

from django.db import models
from django.contrib.auth.models import User

from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.urlresolvers import reverse
from apps.core.templatetags.entry_tags import render_tag
from django.template.loader import render_to_string
from django.db.models import get_model

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from apps.core.models import ThreadedEntry, ThreadedEntryHistory, Entry, EntryHistory
from apps.articles.models import Article

from apps.core.signals import *

import site_strings

''' NEW FORUM '''

class Forum(Entry):
    """
    Forum thread

    """
        
    title = models.CharField(max_length=128, verbose_name = u'Rubrik')
    body = models.TextField(max_length=5120, verbose_name = u'Meddelande', help_text = site_strings.COMMENT_FORM_HELP_TEXT)
    tags = TaggableManager()
    last_comment = models.ForeignKey('ForumComment', null=True, blank=True, default = None, on_delete=models.SET_NULL)
    posts_index = models.IntegerField(null=True, blank=True)

    class Meta:
        permissions = (
            ("access_mod_forum", "Access to mod forum"),
        )
        verbose_name = "Forumtråd"
        verbose_name_plural = "Forumtrådar"

        
    @property
    def get_verbose_name(self):
        return self._meta.verbose_name

    @property
    def ajax_editable_fields(self):
        return ["body"]

    @property
    def is_deleteble(self):
        return False
        
    @property
    def delete_next_url(self):
        return reverse('read_forum', args=[self.id])
        
    @property
    def is_editable(self):
        return True
           
    @property
    def allow_history(self):
        return True    
        
    @property
    def fields_history(self):
        return ["body"]

        
    def aaData(self, request):
        """
        aaData formats for datatables
        """

        title = u"<a href=\"{0}\" >{1}</a>".format( self.get_absolute_url(), self.title )

        subscriptions=request.user.profile.subscriptions.all()
        tags = ""
        for tag in self.tags.all():
            vars = render_tag(tag, '/forum/tag/', subscriptions)
            tags += render_to_string('tag_template.html', vars)

        created = u"{0} {1} av <a href=\"{2}\">{3}</a>".format(naturalday(self.date_created), self.date_created.strftime("%H:%M"), self.created_by.get_profile().get_absolute_url(), self.created_by.username)

        data =  {
                'title': title,
                'tags' : tags,
                'created': created,
                'index' : self.id,
                'posts_index': self.posts_index,
                }

        if self.last_comment:
            last_comment =u"<a href=\"{0}\">{1} {2} av {3}</a>".format(self.last_comment.get_absolute_url(), naturalday(self.last_comment.added), self.last_comment.added.strftime("%H:%M"), self.last_comment.created_by.username)
            data['last_comment'] = last_comment
        else:
            last_comment =u"<a href=\"{0}\">{1} {2} av {3}</a>".format(self.get_absolute_url(), naturalday(self.date_last_changed), self.date_last_changed.strftime("%H:%M"), self.created_by.username)
            data['last_comment'] = last_comment  

        data['date_last_changed'] = time.mktime(self.date_last_changed.timetuple())

        return data
        
        
    def get_posts_index(self):
    
        if not self.posts_index:
            number = ForumComment.objects.filter(post=self).count()
            self.posts_index = number
        
        number = self.posts_index
            
        return number
     
    def get_absolute_url(self):
        return u'{0}'.format( reverse('read_forum', args=[self.id]) )
        
    def __unicode__(self):
        return u'%s' % self.title
 
class ForumComment(MPTTModel):
    post = models.ForeignKey(Forum,blank=True, null=True, on_delete=models.SET_NULL)
    author = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, related_name="created_%(class)s_entries", blank=True, null=True)
    comment = models.TextField(help_text=site_strings.COMMENT_FORM_HELP_TEXT, verbose_name="Kommentar")
    added  = models.DateTimeField(default=datetime.datetime.now,blank=True)
    date_last_changed = models.DateTimeField(auto_now=False, blank=True, null=True)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        super(ForumComment, self).save(*args, **kwargs)

        # Update parent post
        if self.post:
            post = self.post

            # Update post count
            if post.posts_index:
                post.posts_index  += 1
            else:
                post.posts_index = post.get_posts_index()

            # Set last comment
            post.last_comment = self

            # Set last changed
            post.date_last_changed = self.added

            # Save the post
            post.save()

    class Meta:
        permissions = (
            ("access_mod_forum", "Access to mod forum"),
        )
        verbose_name = "Forumkommentar"
        verbose_name_plural = "Forumkommentarer"

    @property
    def get_verbose_name(self):
        return self._meta.verbose_name
        
    def __unicode__(self):
        return u'Kommentar i tråden {0}'.format(self.post)

    def get_absolute_url(self):
        return u'{0}?h=comment-{1}'.format( reverse('read_forum', args=[self.post.id]), self.id)
        

    def get_absolute_url_without_context(self):
        return u'{0}'.format( reverse('read_forum_comment', args=[self.post.id, self.id]) )

    # a link to comment that is being replied, if one exists
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by=['added']

    @property
    def ajax_editable_fields(self):
        return ["comment"]

    @property
    def is_deleteble(self):
        
        deleteble = False
        
        if self.is_root_node():
            deleteble = True
        
        if not self.is_leaf_node():
            deleteble = False
            
        if not self.is_root_node():
            siblings = self.get_siblings(include_self=True).reverse()
            siblings_count = len (siblings)
            
           # If not alone?
            if siblings_count > 1:
                deleteble = False 

            #If last? 
            if siblings[0] == self:
                deleteble = True

        return deleteble
        
    @property
    def delete_next_url(self):
        return reverse('read_forum', args=[self.post.id])
        
    @property
    def is_editable(self):
        """
        Limit is_editable to one day
        """
        return datetime.datetime.now() - self.added < datetime.timedelta(days=1)
           
    @property
    def allow_history(self):
        return True    
        
    @property
    def fields_history(self):
        return ["comment"]
        
    @property
    def get_reply_url(self):
        return reverse('comment_forum', args=[self.post.id])
        
''' END NEW FORUM '''   

class Thread(Entry):
    """
    A collection of ForumPost:s.

    """
    title = models.CharField(max_length=100)
    tags = TaggableManager()
    posts_index = models.IntegerField(null=True, blank=True)
    last_post = models.ForeignKey('ForumPost', null=True, blank=True, default = None)
    
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

class ModeratorForumCategories(models.Model):
    """
    Default categories for the forum
    using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)