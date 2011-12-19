from apps.core.utils import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required(login_url='/auth/login/')
def read_settings(request, appname=None):
    """
    Settings module
    Show setting for users
    
    """
    vars = {
            'appname':appname,
            }

    if appname == "profiles":
        from apps.profiles.views import update_profile
        return update_profile(request)

    return render(request, 'settings.html', vars)