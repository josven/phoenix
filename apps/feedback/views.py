from django.utils.translation import ugettext as _

from django.contrib.sites import models as sites_models

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext

from feedback.forms import FeedbackForm

def leave_feedback(request, template_name='feedback/feedback_form.html'):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.site = sites_models.Site.objects.get_current()
        feedback.save()
        request.user.message_set.create(message=_("Your feedback has been saved successfully."))
        return HttpResponseRedirect(request.POST.get('next', request.META.get('HTTP_REFERER', '/')))
    return render_to_response(template_name, {'feedback_form': form}, context_instance=RequestContext(request))

def ajax_feedback(request):
    data = request.POST.copy()

    res = {
        'status': 'NODATA',
        'errors': None,
    }

    feedback_form = FeedbackForm(data=data)
    if feedback_form.is_bound:
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.site = sites_models.Site.objects.get_current()
            if request.user.id:
                feedback.user = request.user
            feedback.save()

            res = {
                'status': 'OK',
                'errors': None,
            }

        else:
            res = {
                'status': 'NOK',
                'errors': feedback_form.errors,
            }

    return HttpResponse(simplejson.dumps(res), content_type='text/json')

