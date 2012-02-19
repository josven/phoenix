from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',  
  
    #json for datatables
    url(r'^articles/list/json/$', 'apps.articles.views.list_articles_json', name='list_articles_json'),
    url(r'^articles/list/(?P<tags>(.+)(,\s*.+)*)/json/$', 'apps.articles.views.list_articles_json', name='list_articles_json'),  
    url(r'^user/(?P<user_id>\d*)/(?P<tags>(.+)(,\s*.+)*)/json/$', 'apps.articles.views.list_articles_json', name='list_articles_json'),
    url(r'^articles/tag/(?P<tags>(.+)(,\s*.+)*)/json/$', 'apps.articles.views.list_articles_json', name='list_articles_json'),    

    # Return allarticles
    url(r'^articles/list/$', 'apps.articles.views.read_article', name='read_article'),    
    
    # Return a single article
    url(r'^articles/read/(?P<id>\d*)/$', 'apps.articles.views.read_article', name='read_article'),    
    
    # Create
    url(r'^articles/create/$', 'apps.articles.views.create_article', name='create_article'),    
    url(r'^articles/tag/(?P<tags>(.+)(,\s*.+)*)/$', 'apps.articles.views.search_article', name='search_article'),

    #Ajax APIs
    url(r'^articles/(?P<id>\d*)/body/form/$', 'apps.articles.views.ajax_article_body_form', name='ajax_article_body_form'),

    #User url articles
    #url(r'^user/(?P<user_id>\d*)/articles/tag/(?P<tags>(.+)(,\s*.+)*)/$', 'apps.articles.views.search_article', name='read_user_articles'),

    url(r'^user/(?P<user_id>\d*)/article/(?P<id>\d*)/$', 'apps.articles.views.read_article', name='read_user_article'),  
    url(r'^user/(?P<user_id>\d*)/(?P<tags>(.+)(,\s*.+)*)/$', 'apps.articles.views.search_article', name='read_user_articles'),
    
    # Comment articles
    url(r'^articles/(?P<article_id>\d*)/comment/$', 'apps.articles.views.comment_article', name='comment_article'),
  

    
)
