from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^goto_page/$', 'labgeeksrpg.wiki.views.goto_page'),
                       (r'^(?P<page_name>[\w|\W]+)/edit/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>[\w|\W]+)/save/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>[\w|\W]+)/$', 'labgeeksrpg.wiki.views.view_page'),
                       (r'^(?P<page_name>[\w|\W]+)/revisions/$', 'labgeeksrpg.wiki.views.revision_history'),
                       (r'^(?P<page_name>[\w|\W]+)/select_revision/$', 'labgeeksrpg.wiki.views.select_revision'),
                       (r'^$', 'labgeeksrpg.wiki.views.wiki_home'),
                       )
