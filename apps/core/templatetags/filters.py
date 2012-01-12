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

def age(bday, d=None):
    if d is None:
        d = datetime.date.today()
    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))

register.filter('age', age)