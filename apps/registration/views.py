from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from models import BetaReg

from apps.core.utils import render

@require_POST
def register_beta(request):
    """
    Register a beta email address!

    """

    if not request.is_ajax():
        raise Http404

    ip = '0.0.0.0'
    for ipf in ('HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'):
        if ipf in request.META:
            ip = request.META[ipf]
            break

    email = request.POST['email']

    if BetaReg.objects.filter(email=email).exists():
        return HttpResponse('false')

    BetaReg.objects.create(email=email, ip=ip)
    return HttpResponse('true')

def auth_login(request):
    """
    Log in a user
    
    """
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, "Du loggade just in.")
            else:
                messages.add_message(request, messages.INFO, "Ej aktiv användare")
        else:
            messages.add_message(request, messages.INFO, "Fel användarnamn eller lösenord.")
            
    return render(request,'login.html')
    
@login_required(login_url='/auth/login/')
def auth_logout(request):
    """
    Log out a user
    
    """
    messages.add_message(request, messages.INFO, "Du har just loggat ut")
    logout(request)
    return render(request,'login.html')