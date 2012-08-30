from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^goto_page/$', 'labgeeksrpg.wiki.views.goto_page'),
                       (r'^(?P<page_name>[\w ]+)/edit/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>[\w ]+)/save/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>[\w ]+)/$', 'labgeeksrpg.wiki.views.view_page'),
                       (r'^(?P<page_name>[\w ]+)/revisions/$', 'labgeeksrpg.wiki.views.revision_history'),
                       (r'^(?P<page_name>[\w ]+)/select_revision/$', 'labgeeksrpg.wiki.views.select_revision'),
                       (r'^$', 'labgeeksrpg.wiki.views.wiki_home'),
                       )
