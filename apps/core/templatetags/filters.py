import datetime

from django import template
from django.utils.translation import ugettext, ungettext

register = template.Library()


@register.filter(name='minutessince')
def minutessince(date):
    delta = datetime.datetime.now() - date

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return num_minutes

    return 0