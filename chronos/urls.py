from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.chronos.views',
    (r'^report/$', 'report'),
    url(r'^time/$', 'time',name="Time"),
    url(r'^report/(?P<year>\w+)/(?P<month>\w+)/$', 'monthly_report', name="Report-Monthly"),
    url(r'^report/(?P<year>\w+)/(?P<month>\w+)/weekly/(?P<week>\w+)','weekly_report', name="Report-Weekly"),
    url(r'^report/(?P<year>\w+)/(?P<month>\w+)/payperiod/(?P<payperiod>\w+)','payperiod_report', name="Report-Payperiod"),
    url(r'^report/personal/(?P<year>\w+)/(?P<month>\w+)/$','monthly_personal_report', name="Personal-Report_Monthly"),
    url(r'^report/personal/(?P<year>\w+)/(?P<month>\w+)/payperiod/(?P<payperiod>\w+)','personal_payperiod_report', name="Personal-Report-Payperiod"),
    url(r'^report/personal/(?P<year>\w+)/(?P<month>\w+)/weekly/(?P<week>\w+)','personal_weekly_report', name="Personal-Report-Weekly"),
    url(r'^report/personal/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)', 'personal_report_specific',name="Personal-Report-Specific"),
    url(r'^report/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)', 'specific_report',name="Report-Specific"),
    (r'^time/success/$', 'success'),
    (r'^time/fail/', 'fail'),
    (r'^$', 'personal_report'),
)
