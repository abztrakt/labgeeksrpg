from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.people.views',
    url(r'^(?P<name>\w+)/$', 'view_profile', name="People-View_Profile"),
    url(r'^(?P<name>\w+)/edit/$', 'create_user_profile', name="People-Create_Profile"),
    url(r'(?P<name>\w+)/timesheet/$', 'view_timesheet', name="People-View_Timesheet"),
    url(r'(?P<name>\w+)/timesheet/(?P<year>\d+)/(?P<month>\d+)/$', 'view_specific_timesheet', name="People-View_Specific_Timesheet"),
    url(r'(?P<name>\w+)/timesheet/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'view_shifts_timesheet', name="People-View_Shifts_Timesheet"),
    (r'^$', 'list_all'),
)
