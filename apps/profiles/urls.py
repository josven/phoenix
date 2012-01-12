from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^$', 'apps.profiles.views.read_profile', name='read_profile'),
    url(r'^(?P<user_id>\d*)/$', 'apps.profiles.views.read_profile', name='read_profile'),
    
    url(r'^update/$', 'apps.profiles.views.update_profile', name='update_profile'),
    
    #Ajax APIs
    url(r'^(?P<user_id>\d*)/description/form/$', 'apps.profiles.views.profile_description_form', name='ajax_user_description_form'),

)
