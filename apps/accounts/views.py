from apps.core.utils import render
from forms import *
from django.contrib.auth import views as auth_views

def update_account(request):
    """
    Update account settings
    
    """
    form = AccountForm()
    vars = {
            'form':form
            }
    
    return render(request,'update_account.html', vars)