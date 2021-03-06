from django.conf.urls.defaults import patterns, url
from django.conf import urls
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'apps.registration.views.startpage', name='startpage'),
    url(r'^auth/login/$', 'apps.registration.views.auth_login', name='login'),
    url(r'^auth/logout/$', 'apps.registration.views.auth_logout', name='logout'),
    url(r'^auth/register/$', 'apps.registration.views.auth_register', name='register'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),


	url(r'^auth/reset-password/$', 'django.contrib.auth.views.password_reset', kwargs={'email_template_name':'email_reset_password_template.html', 'template_name':'reset_password.html','post_reset_redirect': '/auth/reset-password-done/'}, name='reset_password'), 
	url(r'^auth/reset-password-confirm/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', kwargs={'post_reset_redirect': '/auth/reset-password-complete/', 'template_name':'password_reset_confirm.html', 'extra_context':{'app_name':'registration'}}, name='reset_password_confirm'), 
	url(r'^auth/reset-password-done/$', 'django.contrib.auth.views.password_reset_done', kwargs={'template_name':'reset_password_done.html'}, name='reset_password_done'), 
	url(r'^auth/reset-password-complete/$', 'django.contrib.auth.views.password_reset_complete',kwargs={'template_name':'reset_password_complete.html'}, name='reset_password_complete'), 

)
