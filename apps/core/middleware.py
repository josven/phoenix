# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

class AjaxRedirect(object):
	def process_response(self, request, response):

		if request.is_ajax():
			if str(request.path).find("reset") == -1:
				# Ajax redirect som vi vill följa efter
				if type(response) == HttpResponseRedirect:
					response.status_code = 278

		return response