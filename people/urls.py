from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.people.views',
    (r'^(.*)/$', 'view_profile'),
    (r'^$', 'list_all'),
)
