from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse

from models import BetaReg


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
