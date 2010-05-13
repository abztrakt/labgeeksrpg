from django.conf.urls.defaults import *
import os
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    
    (r'^login/$', 'labgeeksrpg.views.labgeeks_login'),
    (r'^inactive/$', 'labgeeksrpg.views.inactive'),
    
    (r'^success/$', 'labgeeksrpg.views.success'),
    # Example:
    # (r'^labgeeksrpg/', include('labgeeksrpg.foo.urls')),
    (r'^chronos/', include('labgeeksrpg.chronos.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "%s/templates/static" % os.path.realpath('.')}),
    )
