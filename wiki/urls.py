from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^goto_page/$', 'labgeeksrpg.wiki.views.goto_page'),
                       (r'^(?P<slug>[-\w]+)/edit/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<slug>[-\w]+)/save/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<slug>[-\w]+)/$', 'labgeeksrpg.wiki.views.view_page'),
                       (r'^(?P<slug>[-\w]+)/revisions/$', 'labgeeksrpg.wiki.views.revision_history'),
                       (r'^(?P<slug>[-\w]+)/select_revision/$', 'labgeeksrpg.wiki.views.select_revision'),
                       (r'^$', 'labgeeksrpg.wiki.views.wiki_home'),
                       )
