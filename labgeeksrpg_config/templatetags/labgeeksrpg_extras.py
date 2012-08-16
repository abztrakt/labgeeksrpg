from django import template
register = template.Library()

import re
from people.models import UserProfile


@register.simple_tag
def active_tab(request, pattern):
    """ This template tag is used for determining which link in nav.html to highlight in the css.
    """
    is_active = 'nonactive_tab'
    is_home = False
    if request.path == '/':
        is_home = True
    if re.search(pattern, request.path):
        if not pattern == '/chronos' or not re.search('report', request.path):
            is_active = 'active_tab'
    if not is_home and pattern == '/':
        is_active = 'nonactive_tab'
    return is_active


@register.simple_tag
def active_css(request):
    """ This template tag is used for determining which css file to use for the site.
    """
    return 'main.css'
