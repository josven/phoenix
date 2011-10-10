import sys
from django.http import HttpRequest

def find_request():
    f = sys._getframe()
    while f:
        request = f.f_locals.get('request')
        if isinstance(request, HttpRequest):
            break
        f = f.f_back
    return request
