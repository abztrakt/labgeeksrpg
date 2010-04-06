from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.chronos.views',
    (r'^report/$', 'report'),
    (r'^time/$', 'time'),
    (r'^time/success/$', 'success'),
)
