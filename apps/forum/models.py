import datetime

from urllib import quote

from django.db import models
from django.contrib.auth.models import User

from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.urlresolvers import reverse

from django.db.models import get_model

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from apps.core.models import ThreadedEntry, ThreadedEntryHistory, Entry, EntryHistory
from apps.articles.models import Article

from apps.core.signals import *

''' NEW FORUM '''

class Forum(Entry):
    """
    Forum thread

    """
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=5120)
    tags = TaggableManager()
    last_comment = models.ForeignKey('ForumComment', null=True, blank=True, default = None)
    posts_index = models.IntegerField(null=True, blank=True)

        
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

        
    def aaData(self):
        """
        aaData formats for datatables
        """

        title = u"<a href=\"{0}\" >{1}</a>".format( self.get_absolute_url(), self.title )
        tags = [u"<span class=\"ui-tag\"><a href=\"{0}\">{1}</a></span>".format( reverse( 'list_forum', args = [ tag.name ]), unicode(tag.name).title()  ) for tag in self.tags.all()]
        created = u"{0} {1} av <a href=\"{2}\">{3}</a>".format(naturalday(self.date_created), self.date_created.strftime("%H:%M"), self.created_by.get_profile().get_absolute_url(), self.created_by.username)

        data =  {
                'title': title,
                'tags' : u" ".join( tags ),
                'created': created,
                'index' : self.id,
                'posts_index': self.posts_index,

                }


        if self.last_comment:
            last_comment =u"<a href=\"{0}\">{1} {2} av {3}</a>".format(self.last_comment.get_absolute_url(), naturalday(self.last_comment.added), self.last_comment.added.strftime("%H:%M"), self.last_comment.created_by.username)
            data['last_comment'] = last_comment
            data['last_comment_index'] = self.last_comment.id
        else:
            data['last_comment'] = " "
            data['last_comment_index'] = " "
           
        return data
        
        
    def get_posts_index(self):
    
        if not self.posts_index:
            number = ForumComment.objects.filter(post=self).count()
            self.posts_index = number
        
        number = self.posts_index
            
        return number
     
    def get_absolute_url(self):
        return "/forum/read/%s/" % self.id
        
    def __unicode__(self):
        return u'%s' % self.title
 
class ForumComment(MPTTModel):
    post = models.ForeignKey(Forum)
    author = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, related_name="created_%(class)s_entries", blank=True, null=True)
    comment = models.TextField()
    added  = models.DateTimeField(default=datetime.datetime.now,blank=True)
    date_last_changed = models.DateTimeField(auto_now=True, blank=True, null=True)
    tags = TaggableManager()
    
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
        
    def get_absolute_url(self):
        return "/forum/read/{0}/#comment-{1}".format( self.post.id, self.id )
        
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
