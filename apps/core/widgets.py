# -*- coding: utf-8 -*-
from itertools import chain

from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple as DjangoCheckboxSelectMultiple

from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

class CheckboxSelectMultiple(DjangoCheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<div class="tag-wrapper">']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<span class="ui-toggle-button ui-tag">%s<label%s>%s</label></span>' % (rendered_cb, label_for, option_label))

            """
            <input type="checkbox" id="check3" /><label for="check3">U</label>
            """

        output.append(u'</div>')
        return mark_safe(u' '.join(output))