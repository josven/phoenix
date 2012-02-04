from apps.core.utils import render
from forms import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache
@login_required(login_url='/auth/login/')
def update_account(request):
    """
    Update account settings
    
    """
    form = AccountForm()
    vars = {
            'form':form
            }
    
    return render(request,'update_account.html', vars)
    

 

 
class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None