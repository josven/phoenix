from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', direct_to_template, {'template': 'beta.html'}),
    (r'^register/beta/$', 'apps.registration.views.register_beta'),
    (r'^test$', direct_to_template, {'template': 'desktop_base.html'}),
    (r'^auth/', include('apps.registration.urls')),
)
