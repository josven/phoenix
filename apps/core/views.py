# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from apps.core.utils import render

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