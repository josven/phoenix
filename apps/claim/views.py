from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings

import base64

def claim_username(request, key):
    results = {'success':True,
               'key':key,
               'message':"Testsvar"
              }

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')