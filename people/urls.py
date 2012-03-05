from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.people.views',
    url(r'^(?P<name>\w+)/$', 'view_profile', name="People-View_Profile"),
    url(r'^(?P<name>\w+)/edit/$', 'create_user_profile', name="People-Create_Profile"),
    url(r'^(?P<user>\w+)/review/$', 'view_and_edit_reviews', name="People-View_Reviews"),
    url(r'^(?P<user>\w+)/review/info/$', 'view_review_data', name="People-View_Review_Data"),
    (r'^$', 'list_all'),
)
