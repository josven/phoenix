from django.conf import settings

from feedback.forms import FeedbackForm

def feedback_form(request):
    feedback_form = FeedbackForm()

    return {'feedback_form': feedback_form}

