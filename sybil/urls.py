from django.conf.urls.defaults import *
from labgeeksrpg.sybil.views import *

urlpatterns = patterns('labgeeksrpg.sybil.views',
                       url(r'^$', SybilSearch(), name='haystack_search'),
                       )
