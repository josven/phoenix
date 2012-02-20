from django.conf.urls.defaults import patterns, url
from django.conf import urls
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',    
    #url(r'^update/$', 'apps.accounts.views.update_account', name='update_account'),
    #url(r'^update/$', auth_views.password_change, {'template_name' : 'update_account.html'}, name='update_account'),

    url(r'^passreset/$',auth_views.password_reset,name='forgot_password1'),
    url(r'^passresetdone/$',auth_views.password_reset_done,name='forgot_password2'),
    url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='forgot_password3'),
    url(r'^passresetcomplete/$',auth_views.password_reset_complete,name='forgot_password4'),
    
    url(r'^password/change/$', auth_views.password_change, {'template_name' : 'update_account.html'}, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name': 'update_account.html'}, name='auth_password_change_done'),
    
    
    url(r'^list/$', 'apps.accounts.views.list_accounts', name='list_accounts'),
    url(r'^list/json/$', 'apps.accounts.views.list_accounts_json', name='list_accounts_json'),
)