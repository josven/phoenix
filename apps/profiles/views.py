from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from apps.core.utils import render
from models import Profile
from forms import ProfileForm

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

    return render(request, 'profile.html', {"profile": profile, 'user': profile.user})


@login_required(login_url='/auth/login/')
def update_profile(request):
    """
    Updates a profile. Users may only update their own profile.
    
    """
    user = request.user

    profile, created = Profile.objects.select_related().get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print request.FILES

            return HttpResponseRedirect('/user/')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {"profile": profile, 'user': profile.user, 'form':form})
