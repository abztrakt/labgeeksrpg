from django import template
register = template.Library()

import re
from people.models import UserProfile

@register.simple_tag
def active_tab(request, pattern):
    """ This template tag is used for determining which link in nav.html to highlight in the css.
    """

    if re.search(pattern, request.path):
        if not pattern == '/chronos' or not re.search('report',request.path):
            return 'active_tab'
    return 'nonactive_tab'

@register.simple_tag
def active_css(request):
    """ This template tag is used for determining which css file to use for the site.
    """
    try:
        profile = UserProfile.objects.get(user=request.user) 
        if profile.site_skin:
            return profile.site_skin
        return 'main.css'
    except:
        return 'main.css'
