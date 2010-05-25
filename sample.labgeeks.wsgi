import os, sys

sys.path.append('/var/django')
sys.path.append('/var/django/labgeeksrpg')

os.environ['DJANGO_SETTINGS_MODULE'] = 'labgeeksrpg.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
