import sys, inspect
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render as djangorender

def find_request():
    """
    Find the request object and return it. For use when we dont have a propper
    request object to go to. Will contain all the usual stuff.
    
    """
    f = sys._getframe()
    while f:
        request = f.f_locals.get('request')
        if isinstance(request, HttpRequest):
            break
        f = f.f_back
    return request

def set_base_template(request,base):
    print base
    if base == 'touch':
        request.session['base_template'] = 'touch_base.html'
    else:
        request.session['base_template'] = 'desktop_base.html'

    try:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except:
        return HttpResponseRedirect(request.META['PATH_INFO'])
    
def get_base_template(request):
    try:
        return request.session['base_template']
    except:
        request.session['base_template'] = 'desktop_base.html'
        return request.session['base_template']
        
def render(request,*args):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    template = args[0]
    
    try:
        vars = args[1]
    except:
        vars = {}
    
    vars['app_name'] = mod.__name__.split('.')[1]
    vars['base_template'] = get_base_template(request)
    return djangorender(request,template,vars)
    

