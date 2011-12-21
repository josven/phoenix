from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',    
    # Return a single article
    url(r'^$', 'apps.articles.views.read_article', name='read_article'),    
    url(r'^(?P<id>\d*)/$', 'apps.articles.views.read_article', name='read_article'),    
    
    url(r'^create/$', 'apps.articles.views.create_article', name='create_article'),    
    url(r'^tag/(?P<tags>\w*)/$', 'apps.articles.views.search_article', name='search_article'),    
    
    #Ajax APIs
    url(r'^(?P<id>\d*)/body/form/$', 'apps.articles.views.ajax_article_body_form', name='ajax_article_body_form'),

)
