from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


# Resoures
from apps.mobile.api import UserResource
from apps.mobile.api import ChatEntryResource
from apps.mobile.api import ForumThreadResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(ChatEntryResource())
v1_api.register(ForumThreadResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^mobile/', include('apps.mobile.urls')),
    (r'^', include('apps.registration.urls')),
    (r'^', include('apps.frontpage.urls')),
    (r'^', include('apps.core.urls')),
    (r'^', include('apps.settings.urls')),
    (r'^', include('apps.guestbook.urls')),

    (r'^forum/', include('apps.forum.urls')),
    (r'^user/', include('apps.profiles.urls')),
    (r'^chat/', include('apps.chat.urls')),
    (r'^claim/', include('apps.claim.urls')),
    (r'^notifications/', include('apps.notifications.urls')),
    (r'^', include('apps.articles.urls')),
    (r'^accounts/', include('apps.accounts.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
