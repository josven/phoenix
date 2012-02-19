# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.db.models import get_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from apps.core.utils import render
from forms import update_entry_form, delete_entry_form, subscribe_tag_form

from reversion.models import Version


@never_cache
@login_required(login_url='/auth/login/')
def subscribe_tag(request):
    if request.method == 'POST':
        if request.is_ajax():
            form = subscribe_tag_form(request.POST)
            
            if form.is_valid():
                
                #Get user
                user = request.user
                profile = request.user.get_profile()
                new_tag = unicode(form.cleaned_data['tag'])
                usertags =  [tag.name for tag in profile.subscriptions.all()]
                if new_tag in usertags:
                    profile.subscriptions.remove(new_tag)
                    data = {
                            'tag_status':0,
                            'message': u'Tog bort bevakning för <strong>\"{0}\"</stong>'.format(new_tag)
                            }
                else:
                    profile.subscriptions.add(new_tag)
                    data = {
                            'tag_status':1,
                            'message': u'Du bevakar nu <strong>\"{0}\"</stong>'.format(new_tag)
                            }             
                
                return HttpResponse(simplejson.dumps(data), content_type="application/json")
    
    return HttpResponse(status=404)

@never_cache
@login_required(login_url='/auth/login/')
def preview(request):

	if request.method == 'POST':

		if request.is_ajax():
				
				preview_id = request.POST.get('preview', None)
				
				if preview_id:
				
					preview = request.POST.get(preview_id, None)
					
					if preview:
						
						return render(request, 'preview.html', {'preview':preview} )

	return HttpResponse(status=404)
    
@never_cache
@login_required(login_url='/auth/login/')   
def update_entry(request, app_label, class_name, id):   
    vars = {}

    # Check if theres an valid instance
    try:
        model = get_model(app_label, class_name)
        if model:
            instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404) # No valid instance
        
    # Check if user can edit instance
    if instance.created_by != request.user:
        HttpResponse(status=401) # User not auth
        
        
    # if there any fields to edit
    if not instance.ajax_editable_fields:
        return HttpResponse(status=404) # No field to edit

    
    if request.method == 'GET':

        # Get form
        fields = instance.ajax_editable_fields
        form = update_entry_form( fields, model, instance=instance)
        vars['form'] = form
    
    if request.method == 'POST':
        fields = instance.ajax_editable_fields
        form = update_entry_form( fields, model, request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        
        return HttpResponse(status=401)
        
        
    return render(request, 'update_entry_form.html', vars ) 
    
@never_cache
@login_required(login_url='/auth/login/')   
def delete_entry(request, app_label, class_name, id):   
    vars = {}

    # Check if theres an valid instance
    try:
        model = get_model(app_label, class_name)
        if model:
            instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404) # No valid instance
        
    # Check if user can delete instance
    if instance.created_by != request.user and instance.is_deleteble:
        HttpResponse(status=401) # User not auth

    if request.method == 'GET':
        # Get form
        form = delete_entry_form()
        vars['form'] = form
    
    if request.method == 'POST':
        form = delete_entry_form( request.POST )
        
        if form.is_valid():
            instance.delete()
            return HttpResponse(status=200)
        
        return HttpResponse(status=428)
        
        
    return render(request, 'update_entry_form.html', vars )

@never_cache
@login_required(login_url='/auth/login/')   
def history_entry(request, app_label, class_name, id):   
    vars = {}

    # Check if theres an valid instance
    try:
        model = get_model(app_label, class_name)
        if model:
            instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404) # No valid instance
        
    # Check if history is allowed
    if instance.allow_history and instance.fields_history:
        versions = Version.objects.get_for_object(instance)
        history_diff = []
        for version in versions:
            for field in instance.fields_history:
                history = version.field_dict.get(field, None)
                current = instance.__dict__.get(field, None)
                if history != current:
                    history_diff += [{'content':history,'date':version.revision.date_created}]

        
        vars['history'] = history_diff #versions #Version.objects.get_for_object(instance)
    else:
        return HttpResponse(status=401) # Not allowed
        
    return render(request, 'history_entry_template.html', vars )