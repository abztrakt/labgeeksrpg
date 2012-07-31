from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^(?P<page_name>\w+)/edit/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>\w+)/save/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>\w+)/$', 'labgeeksrpg.wiki.views.view_page'),
                       (r'^(?P<page_name>\w+)/revisions/$', 'labgeeksrpg.wiki.views.revision_history'),
                       (r'^$', 'labgeeksrpg.wiki.views.wiki_home'),
                       )
