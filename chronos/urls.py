from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.chronos.views',
    (r'^report/$', 'report'),
    url(r'^report/(?P<year>\w+)/(?P<month>\w+)/$', 'monthly_report', name="Report-Monthly"),
    url(r'^report/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)', 'specific_report',name="Report-Specific"),
    (r'^time/$', 'time'),
    (r'^time/success/$', 'success'),
    (r'^time/fail/', 'fail'),
    (r'^$', 'personal_report'),
)
