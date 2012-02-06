import datetime

from django import template
from django.utils.translation import ugettext, ungettext
from django.template.defaultfilters import stringfilter
from oembed.core import replace

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






@stringfilter
def my_oembed(input, args):
    args = args.split()
    if len(args) > 1:
        raise template.TemplateSyntaxError("Oembed tag takes only one (option" \
            "al) argument: WIDTHxHEIGHT, where WIDTH and HEIGHT are positive " \
            "integers.")
    if len(args) == 1:
        width, height = args[0].lower().split('x')
        if not width and height:
            raise template.TemplateSyntaxError("Oembed's optional WIDTHxHEIGH" \
                "T argument requires WIDTH and HEIGHT to be positive integers.")
    else:
        width, height = None, None
    kwargs = {}
    if width and height:
        kwargs['max_width'] = width
        kwargs['max_height'] = height
        
    return replace(input, **kwargs)

register.filter('my_oembed', my_oembed)