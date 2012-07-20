# -*- coding: utf-8 -*-
from django.template.loader import render_to_string

from taggit.managers import TaggableManager as OrginalTaggableManager
from taggit.managers import _TaggableManager as Orginal_TaggableManager

from apps.core.templatetags.entry_tags import render_tag
from apps.core.forms import subscribe_tag_form

class TaggableManager(OrginalTaggableManager):
    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                "before you can access their tags." % model.__name__)
        manager = _TaggableManager(
            through=self.through, model=model, instance=instance
        )
        return manager

class _TaggableManager(Orginal_TaggableManager):
    def render_html(self):
        
        tags = self.all()
        tag_search_prefix = u"/{0}/tag/".format(self.instance.__class__.__module__.split('.')[1])
        html = ""
        for tag in tags:
            html += render_to_string('tag_template.html',{"tag":tag, "tag_search_prefix":tag_search_prefix, "subscribe_tag_form":subscribe_tag_form(initial={'tag':tag})})
        
        return html
