from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, Http404
from django.views.decorators.cache import never_cache

from apps.core.utils import render
from models import Profile
from forms import * #ProfileForm, ProfileDescriptionForm, ProfileSubscriptionsForm

@never_cache
@login_required(login_url='/auth/login/')
def read_profile(request, user_id=None):
    """
    Read a profile. Uses the profile of the current user if not given an id.
    
    Note that this takes user id and not profile id. It is good practice to
    never select anything based on profile.
    """
    # Get the user
    if not user_id:
        user = request.user
    else:
        user = User.objects.get(pk=user_id)
    profile, created = Profile.objects.select_related().get_or_create(user=user)
    
    if request.is_ajax():
        template = '_profile.html'
    else:
        template = 'profile.html'
        
    return render(request, template, {"profile": profile,'user':user})
    
@never_cache
@login_required(login_url='/auth/login/')
def update_profile(request):
    """
    Updates a profile. Users may only update their own profile.
    
    """

    profile, created = Profile.objects.select_related().get_or_create(user=request.user)
    if request.method == 'POST':
        if 'profile-form' in request.POST:
            print 'profile-form'
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            SubscriptionsForm = ProfileSubscriptionsForm(instance=profile)
            
            if form.is_valid():
                form.save()
                
                return HttpResponseRedirect('/user/')
            
        if 'profile-subscriptions-form' in request.POST:            
            form = ProfileForm(instance=profile)
            SubscriptionsForm = ProfileSubscriptionsForm(request.POST, request.FILES, instance=profile)
            
            if SubscriptionsForm.is_valid():
                SubscriptionsForm.save()
                
                return HttpResponseRedirect('/user/')
    else:
        form = ProfileForm(instance=profile)
        SubscriptionsForm = ProfileSubscriptionsForm(instance=profile)

    vars = {
            "profile": profile,
            'user': profile.user,
            'form':form,
            'SubscriptionsForm':SubscriptionsForm,
            }
  
    return render(request, 'update_profile.html', vars)

@never_cache    
@login_required(login_url='/auth/login/')
def profile_description_form(request,user_id=None):
    user = request.user
    profile, created = Profile.objects.select_related().get_or_create(user=user)
    
    if request.method == 'POST':
        form = ProfileDescriptionForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    action = reverse('ajax_user_description_form', args=[user.id])
    form = ProfileDescriptionForm(instance=profile)
    
    return render(request, 'ajaxform.html', {'form':form,'action':action})

    
        
   