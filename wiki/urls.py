from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^(?P<page_name>\w+)/edit/$', 'labgeeksrpg.wiki.views.edit_page'),
                       (r'^(?P<page_name>\w+)/save/$', 'labgeeksrpg.wiki.views.save_page'),
                       (r'^(?P<page_name>\w+)/$', 'labgeeksrpg.wiki.views.view_page'),
                       (r'^$', 'labgeeksrpg.wiki.views.wiki_home'),
                       )
