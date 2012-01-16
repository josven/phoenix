from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
    vars = {
        'body_id':'page_login'
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            '''
            if not user.is_staff:
                messages.add_message(request, messages.INFO, "Siten inte öppen.")
                return render(request, 'comming_soon.html')
            '''
            
            if user.is_active:
                login(request, user)
                request.session.set_expiry(0)
                messages.add_message(request, messages.INFO, "Du loggade just in.")

                return HttpResponseRedirect(reverse('start'))
                
            else:
                messages.add_message(request, messages.INFO, "Ej aktiv användare")
        else:
            messages.add_message(request, messages.INFO, "Fel användarnamn eller lösenord.")

    return render(request, 'login.html')

@login_required(login_url='/auth/login/')
def auth_logout(request):
    """
    Log out a user
    
    """
    messages.add_message(request, messages.INFO, "Du har just loggat ut")
    logout(request)
    return render(request, 'login.html')


def auth_register(request):
    """
    register a user
    
    """
    
    #return render(request,'comming_soon.html')
    
    
    vars = {
        'body_id':'page_register'
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            try:
                User.objects.get(username__iexact=username)
                vars['form'] = form
                messages.add_message(request, messages.INFO, "Användare {0} finns redan.".format( unicode( username ) ) )
                return render(request, 'register.html', vars)
            
            except:
                form.save()
                form = AuthenticationForm()
                messages.add_message(request, messages.INFO, "Användare skapad.")
                user = authenticate(username=username, password=password)
                login(request, user)
                
                return HttpResponseRedirect(reverse('start'))
                
        else:
            messages.add_message(request, messages.INFO, "Fel fel fel fel")
    else:
        form = RegisterForm()

    vars['form'] = form
    return render(request, 'register.html', vars)