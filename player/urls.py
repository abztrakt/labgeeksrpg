from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.player.views',
    # Example:
    # (r'^labgeeksrpg/', include('labgeeksrpg.foo.urls')),
    (r'^$', 'list'),
    (r'^(?P<player>.*)$', 'detail'),
)
