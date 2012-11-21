# -*- coding: utf-8 -*-
from datetime import timedelta

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.edit import ModelFormMixin
from django.views.generic.edit import UpdateView

import site_settings

from apps.mobile.forms import AuthenticationForm
from apps.mobile.forms import UserCreationForm
from apps.mobile.forms import ChatForm
from apps.mobile.forms import ChatSettingsForm

from apps.profiles.models import Profile
from apps.chat.models import Post as ChatEntry
from apps.mobile.models import mobile_settings
from apps.forum.models import Forum as ForumThread
from apps.forum.models import defaultCategories as DefaultForumCategories



"""

    Custom class based views and mixins
    ===================================

"""
class SetPageTitleMixin(object):
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs = super(SetPageTitleMixin, self).get_context_data(**kwargs)
        kwargs.update({'page_title':self.get_page_title()})
        return kwargs

    def get_page_title(self):
        if self.page_title is None:
            raise ImproperlyConfigured(u"You missing a page title, define page_title in your view class")
        return self.page_title

"""

    Login/register/recover/about
    ============================

"""

@never_cache
def login(request):

    vars = {
        'page_title' : 'login',
        'AuthenticationForm' : AuthenticationForm(data = request.POST or None),
        'nextpage': request.GET.get('next', reverse_lazy('mobile_start')),
    }

    if request.method == 'POST':
        if vars['AuthenticationForm'].is_valid():
            user = vars['AuthenticationForm'].get_user()

            if user.is_active:
                user_login(request, user)

                if request.POST.get('keep_session', None):
                    request.session.set_expiry(timedelta(days=365))
                else:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(vars['nextpage'])

    return render(request,'mobile_login.html', vars)

@never_cache
def register(request):

    vars = {
        'page_title' : 'register',
        'UserCreationForm': UserCreationForm( data = request.POST or None ),
        'nextpage': request.GET.get('next', reverse_lazy('mobile_start')),
    }

    if request.method == 'POST':
        if vars['UserCreationForm'].is_valid():
            
            username = vars['UserCreationForm'].cleaned_data['username']
            password = vars['UserCreationForm'].cleaned_data['password1']

            # Kolla om det redan finns en användare med samma namn            
            #if User.objects.filter(username__iexact=username).exists():
            #    return render(request, 'register.html', vars)
            
            vars['UserCreationForm'].save()
            user = authenticate(username=username, password=password)
            user_login(request, user)
            profile, created = Profile.objects.get_or_create(user=user)
            return HttpResponseRedirect(vars['nextpage'])

    return render(request,'mobile_register.html', vars)

@never_cache
def recover(request):

    vars = {
        'page_title' : 'recover',
        'PasswordResetForm':PasswordResetForm( data = request.POST or None ),
    }

    if request.method == 'POST':
        if vars['PasswordResetForm'].is_valid():
            vars['PasswordResetForm'].save()

    return render(request,'mobile_recover.html', vars)


@never_cache
def about(request):

    vars = {
        "page_title" : "about"
    }

    return render(request,'mobile_about.html', vars)


"""

    Start/logout/chat
    =================
    
"""

@login_required(login_url='/mobile/login/')
@never_cache
def start(request):

    vars = {
        "page_title" : "start"
    }

    return render(request,'mobile_start.html', vars)

@login_required(login_url='/mobile/login/')
def logout(request):
    """
    Log out a user
    
    """
    user_logout(request)
    return HttpResponseRedirect( reverse_lazy('mobile_login') )


class ChatView(SetPageTitleMixin, FormView):
    template_name = 'mobile_chat.html'
    form_class = ChatForm
    page_title = "chat"

    @method_decorator(never_cache)
    @method_decorator(login_required( login_url = reverse_lazy( 'mobile_login' )))
    def dispatch(self, *args, **kwargs):
        return super(ChatView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ChatView, self).get_context_data(**kwargs)
        queryset = ChatEntry.active.order_by('-date_created').select_related('created_by','created_by__profile__photo').order_by('-id')[:site_settings.CHAT_LIST_ITEM_LIMIT]
        kwargs.update({'object_list':queryset})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('mobile_chat')

    def form_valid(self, form):
        form.save()
        return super(ChatView, self).form_valid(form)

class ChatSettingsView(SetPageTitleMixin, UpdateView):
    template_name = 'mobile_chat_settings.html'
    form_class = ChatSettingsForm
    page_title = "chat_settings"
    model = mobile_settings
    page_title = "chat_settings"

    @method_decorator(never_cache)
    @method_decorator(login_required( login_url = reverse_lazy( 'mobile_login' )))
    def dispatch(self, *args, **kwargs):
        return super(ChatSettingsView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(user = self.request.user)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            obj = mobile_settings.objects.create( user = self.request.user )
        return obj

    def get_success_url(self):
        return reverse_lazy('mobile_chat')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ChatSettingsView, self).form_valid(form)


class ForumListView(SetPageTitleMixin, ListView):
    context_object_name = 'forum_list'
    queryset = ForumThread.objects.all().order_by("-date_created")
    template_name = 'mobile_forum_list.html'
    page_title = "forum-list"

    @method_decorator(never_cache)
    @method_decorator(login_required( login_url = reverse_lazy( 'mobile_login' )))
    def dispatch(self, *args, **kwargs):
        return super(ForumListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['default_categories'] = DefaultForumCategories.objects.all()
        context['user_categories'] = self.request.user.profile.subscriptions.all()
        return context