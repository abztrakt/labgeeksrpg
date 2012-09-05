from django.conf.urls.defaults import *
from labgeeksrpg.sybil.views import *

urlpatterns = patterns('labgeeksrpg.sybil.views',
                       url(r'^search/$', SybilSearch(), name='haystack_search'),
                       url(r'^$', 'oracle_home', name='oracle_home'),
                       url(r'^upload_image/$', 'upload_image', name='upload_image'),
                       url(r'^screenshots/$', 'view_all_screenshots', name='view_all_screenshots'),
                       )
