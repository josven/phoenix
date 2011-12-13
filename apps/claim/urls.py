from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^(?P<key>\w+)/$', 'apps.claim.views.claim_username', name='claim_username'),
)
