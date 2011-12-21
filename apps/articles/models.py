from django.db import models
from taggit.managers import TaggableManager

from apps.core.models import Entry

class Article(Entry):
    """
    Articles

    """
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=5120)
    tags = TaggableManager()

    def get_absolute_url(self):
        return "/articles/read/%s/" % self.id
        
    def __unicode__(self):
        return u'%s' % self.title

class defaultArticleCategories(models.Model):
    """
    Default categories for the forum
    using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)