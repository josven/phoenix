from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^utils/preview/$', 'apps.core.views.preview', name='preview'),
    url(r'^utils/update-entry/(?P<app_label>\w*)/(?P<class_name>\w*)/(?P<id>\d*)/$', 'apps.core.views.update_entry', name='update_entry'),
    url(r'^utils/delete-entry/(?P<app_label>\w*)/(?P<class_name>\w*)/(?P<id>\d*)/$', 'apps.core.views.delete_entry', name='delete_entry'),
    url(r'^utils/history-entry/(?P<app_label>\w*)/(?P<class_name>\w*)/(?P<id>\d*)/$', 'apps.core.views.history_entry', name='history_entry'),
)
