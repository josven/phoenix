from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apps.registration.views.auth_login', name='start'),
    #(r'^register/beta/$', 'apps.registration.views.register_beta'),
    #(r'^test$', direct_to_template, {'template': 'desktop_base.html'}),
    (r'^core/', include('apps.core.urls')),
    (r'^auth/', include('apps.registration.urls')),
    (r'^forum/', include('apps.forum.urls')),
    (r'^user/', include('apps.profiles.urls')),
    (r'^chat/', include('apps.chat.urls')),
    (r'^claim/', include('apps.claim.urls')),
    (r'^', include('apps.guestbook.urls')),
)
