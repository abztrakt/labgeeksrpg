from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'labgeeksrpg.delphi.views.kb_home'),
                       (r'^create/$', 'labgeeksrpg.delphi.views.create_question'),
                       (r'^(?P<q_id>[\d]+)/$', 'labgeeksrpg.delphi.views.view_question'),
                       (r'^(?P<q_id>[\d]+)/answer/$', 'labgeeksrpg.delphi.views.answer_question'),
                       (r'^(?P<q_id>[\d]+)/select_answer/$', 'labgeeksrpg.delphi.views.select_answer'),
                       )
