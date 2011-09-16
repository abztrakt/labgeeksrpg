from django import template

register = template.Library()

@register.simple_tag
def active_tab(request, pattern):
    """ This template tag is used for determining which link in nav.html to highlight in the css.
    """
    import re

    if re.search(pattern, request.path):
        if not pattern == '/chronos' or not re.search('report',request.path):
            return 'active_tab'
    return 'nonactive_tab'
