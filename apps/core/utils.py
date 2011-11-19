import sys
from django.http import HttpRequest

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
