from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^user/(?P<userid>\d*)/guestbook/$', 'apps.guestbook.views.guestbook', name='guestbook'),
    url(r'^user/(?P<userid>\d*)/guestbook/(?P<start>\d*)$', 'apps.guestbook.views.guestbook', name='guestbook'),
 )
