from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^create_page?/$', 'labgeeksrpg.pythia.views.edit_page'),
                       (r'^(?P<slug>[-\w]+)/edit/$', 'labgeeksrpg.pythia.views.edit_page'),
                       (r'^(?P<slug>[-\w]+)/save/$', 'labgeeksrpg.pythia.views.edit_page'),
                       (r'^(?P<slug>[-\w]+)/$', 'labgeeksrpg.pythia.views.view_page'),
                       (r'^(?P<slug>[-\w]+)/revisions/$', 'labgeeksrpg.pythia.views.revision_history'),
                       (r'^(?P<slug>[-\w]+)/select_revision/$', 'labgeeksrpg.pythia.views.select_revision'),
                       (r'^$', 'labgeeksrpg.pythia.views.pythia_home'),
                       )
