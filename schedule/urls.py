from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.schedule.views',
    url(r'^view_preferences/$', 'view_preferences', name="Schedule-View_Prefs"),
    url(r'^preferences/$', 'edit_preferences', name="Schedule-Edit_Prefs"),
    url(r'^create/$', 'create_default_daily_schedule', name="Schedule-Create_Schedule"),
    url(r'^shifts/$', 'view_shifts', name="Schedule-View_Shifts"),
    url(r'^available/$','view_available_shifts', name="Schedule-View_Avail"),
    url(r'^timeperiods/$','view_timeperiods',name="Schedule-View_Timeperiods"),
    (r'^$','list_options'),
)
