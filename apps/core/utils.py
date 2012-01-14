import sys, inspect
from django.db import models
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render as djangorender
from tracking.models import Visitor

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

def set_base_template(request, base):
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

def render(request, *args):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    template = args[0]

    try:
        vars = args[1]
    except:
        vars = {}
        
    try:
        app_name = vars['app_name']
    except:
        app_name = mod.__name__.split('.')[1]
    
    vars['app_name'] = app_name
    vars['base_template'] = get_base_template(request)
    
    users = Visitor.objects.active()
    seen = set()
    seen_add = seen.add
    vars['active_users'] = [ x for x in users if x.user not in seen and not seen_add(x.user)]
    
    request.session['app_name'] = vars['app_name']
    
    return djangorender(request, template, vars)


def create_datepicker(form):
    formfield = form.formfield()
    if isinstance(form, models.DateField):
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield

def validate_internal_tags(request, tags):

    tags_array = []
    
    for tag in tags:
        is_upper = tag.isupper()
        is_staff = request.user.is_staff
        
        if is_upper and is_staff:
            tags_array.append( tag.upper() )
        else:
            tags_array.append( tag.lower() )
            
    return tags_array