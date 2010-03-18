from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^labgeeksrpg/', include('labgeeksrpg.foo.urls')),
    (r'^chronos/', include('labgeeksrpg.chronos.urls')),
    (r'^players/', include('labgeeksrpg.player.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # COMMENT THIS OUT IN PRODUCTION!!!
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/craig/Documents/Code/django/labgeeksrpg/templates/static'}),
)
