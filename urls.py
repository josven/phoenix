from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('apps.frontpage.urls')),
    #url(r'^$', 'apps.registration.views.auth_login', name='start'),
    (r'^', include('apps.settings.urls')),
    (r'^', include('apps.guestbook.urls')),
    #(r'^register/beta/$', 'apps.registration.views.register_beta'),
    #(r'^test$', direct_to_template, {'template': 'desktop_base.html'}),
    (r'^core/', include('apps.core.urls')),
    (r'^auth/', include('apps.registration.urls')),
    (r'^forum/', include('apps.forum.urls')),
    (r'^user/', include('apps.profiles.urls')),
    (r'^chat/', include('apps.chat.urls')),
    (r'^claim/', include('apps.claim.urls')),
    (r'^articles/', include('apps.articles.urls')),
    (r'^accounts/', include('apps.accounts.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))