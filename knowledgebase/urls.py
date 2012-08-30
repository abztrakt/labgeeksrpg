from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^(?P<issue_name>[\w ]+)/create/$', 'labgeeksrpg.knowledgebase.views.create_issue'),
                       (r'^(?P<issue_name>[\w ]+)/$', 'labgeeksrpg.knowledgebase.views.view_issue'),
                       # (r'^(?P<issue_name>[\w ]+)/solve/$', 'labgeeksrpg.knowledgebase.views.solve_issue'),
                       # (r'^(?P<issue_name>[\w ]+)/select_solution/$', 'labgeeksrpg.knowledgebase.views.select_solution'),
                       )
