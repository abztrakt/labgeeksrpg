from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.schedule.views',
    url(r'^view_preferences/$', 'view_preferences', name="Schedule-View_Prefs"),
    url(r'^preferences/$', 'edit_preferences', name="Schedule-Edit_Prefs"),
    (r'^$','list_options'),
)
