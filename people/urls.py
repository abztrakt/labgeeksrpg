from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.people.views',
    url(r'^(?P<name>\w+)/$', 'view_profile', name="People-View_Profile"),
    url(r'^(?P<name>\w+)/edit/$', 'create_user_profile', name="People-Create_Profile"),
    (r'^$', 'list_all'),
)
