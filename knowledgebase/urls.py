from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'labgeeksrpg.knowledgebase.views.kb_home'),
                       (r'^create/$', 'labgeeksrpg.knowledgebase.views.create_question'),
                       (r'^(?P<q_id>[\d]+)/$', 'labgeeksrpg.knowledgebase.views.view_question'),
                       # (r'^(?P<q_id>[\d]+)/answer/$', 'labgeeksrpg.knowledgebase.views.answer_question'),
                       # (r'^(?P<q_id>[\d]+)/select_answer/$', 'labgeeksrpg.knowledgebase.views.select_answer'),
                       )
