# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from django.utils.html import urlize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib.markup.templatetags.markup import textile

from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource
from tastypie.resources import ALL
from tastypie.resources import ALL_WITH_RELATIONS
from tastypie.cache import NoCache

from sorl.thumbnail import get_thumbnail
from oembed.core import replace as oembed_replace

from apps.core.templatetags.filters import user_filter

from apps.chat.models import Post as ChatEntry
from apps.mobile.models import mobile_settings
from apps.forum.models import Forum as ForumThread


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']

class ForumThreadResource(ModelResource):
    class Meta:
        cache = NoCache()
        queryset = ForumThread.active.all().order_by("-date_created")
        resource_name = 'forum/thread'
        excludes = ['date_deleted']
        filtering = {
            'id': ALL,
            'title': ALL,
            'date_created': ALL,
            'date_last_changed': ALL,
            'tags': ALL,
            }
        ordering = {
            'date_created': ALL,
            'date_last_changed': ALL,
        }
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        bundle.data['date_last_changed'] = u"{0} {1}".format( naturalday( bundle.obj.date_last_changed ), bundle.obj.date_last_changed.strftime("%H:%M") )
        bundle.data['date_created'] = u"{0} {1}".format( naturalday( bundle.obj.date_created ), bundle.obj.date_created.strftime("%H:%M") )
        bundle.data['created_by'] = bundle.obj.created_by.username
        subscriptions = bundle.request.user.profile.subscriptions.all()
        bundle.data['tags'] = u"&nbsp;".join([u'<a class="link-thread-tag" data-subscribe="{2}" data-tag="{0}" href="#popup-tag">{1}</a>'.format(tag.name.replace(" ","_"), tag, tag in subscriptions) for tag in bundle.obj.tags.all()] )

        return bundle

    def apply_authorization_limits(self, request, object_list):
        if not request.user.has_perm('forum.access_mod_forum'):
            object_list = object_list.exclude(tags__name="MOD")
        return object_list

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ForumThreadResource, self).build_filters(filters)

        if 'tag' in filters:
            if filters['tag']:
                orm_filters['tags__name__in'] = filters['tag'].replace("_"," ").split(',')

        return orm_filters

class ChatEntryResource(ModelResource):

    def dehydrate(self, bundle):
        if not bundle.obj.created_by.profile.photo:
            bundle.data['profile_photo'] = None
        else:
            im = get_thumbnail(bundle.obj.created_by.profile.photo, '80x80', crop='center', quality=99)
            bundle.data['profile_photo'] = im.url

        bundle.data['date_created'] = u"{0} {1}".format( naturalday( bundle.obj.date_created ), bundle.obj.date_created.strftime("%H:%M") )
        bundle.data['created_by'] = bundle.obj.created_by.username
        
        settings, created = mobile_settings.objects.get_or_create( user = bundle.request.user )
        if created:
            settings = created

        if settings.chat_oembed:
            # Apply oEmbed
            oembed_kwargs = {}
            oembed_kwargs['max_width'] = 320
            oembed_kwargs['max_height'] = 240
            bundle.data['text'] = oembed_replace(bundle.data['text'], **oembed_kwargs)

        if settings.chat_urlize:
            bundle.data['text'] = urlize(bundle.data['text'], nofollow=True, autoescape=True)

        if settings.chat_textile:
            bundle.data['text'] = textile(bundle.data['text'])

        bundle.data['text'] = u"<p>{0}</p>".format(bundle.data['text'])
        
        if u"@{0}".format(bundle.request.user.username.upper()) in bundle.obj.text.upper():
            bundle.data['data_theme'] = "d"
        else:
            bundle.data['data_theme'] = "c"
        return bundle

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(ChatEntryResource, self).dispatch(*args, **kwargs)

    class Meta:
        queryset = ChatEntry.active.order_by('-date_created')
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        resource_name = 'chat/entry'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        ordering = ['date_created']
        excludes = ['date_deleted', 'date_last_changed']
        filtering = {
            'id': ALL,
            'date_created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            }