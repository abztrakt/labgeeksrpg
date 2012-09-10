from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.chronos.views',
                       (r'^report$', 'report'),
                       url(r'^time/$', 'time', name="Time"),
                       url(r'^report/(?P<year>\w+)/(?P<month>\w+)/$', 'report', name="Report-Monthly"),
                       url(r'^report/(?P<year>\w+)/(?P<month>\w+)/week/(?P<week>\w+)', 'staff_report', name="Report-Weekly"),
                       url(r'^report/(?P<year>\w+)/(?P<month>\w+)/payperiod/(?P<payperiod>\w+)', 'staff_report', name="Report-Payperiod"),
                       url(r'^report/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)', 'staff_report', name="Report-Specific"),
                       (r'^time/success/$', 'success'),
                       (r'^time/fail/', 'fail'),
                       url(r'^(?P<year>\w+)/(?P<month>\w+)/$', 'personal_report', name="Personal-Report-Monthly"),
                       url(r'^(?P<user>\w+)/(?P<year>\w+)/(?P<month>\w+)/payperiod/(?P<payperiod>\w+)', 'specific_report', name="Personal-Report-Payperiod"),
                       url(r'^(?P<user>\w+)/(?P<year>\w+)/(?P<month>\w+)/week/(?P<week>\w+)', 'specific_report', name="Personal-Report-Weekly"),
                       url(r'^(?P<user>\w+)/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)', 'specific_report', name="Personal-Report-Specific"),
                       url(r'^(?P<user>\w+)', 'personal_report', name="Personal-Timesheet"),
                       (r'^$', 'personal_report'),
                       )
