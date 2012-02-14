# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from apps.core.utils import render
from forms import update_entry_form

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
        return HttpResponse(status=404)
        
    # Check if user can edit
    if instance.created_by == request.user:
            field_to_edit = instance.editable_field
            content = getattr(instance, field_to_edit, None)            
    else:
        return HttpResponse(status=401) # User not auth
    
    if request.method == 'GET':
        if content:
            vars['form'] = update_entry_form({'content': content})
        else:
            return HttpResponse(status=404) # No content to edit
    
    if request.method == 'POST':
        form = update_entry_form(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            setattr(instance,field_to_edit,content)
            instance.save()
            return HttpResponse(status=200)

        return HttpResponse(status=401)
        
        
    return render(request, 'update_entry_form.html', vars )