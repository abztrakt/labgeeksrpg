from django.conf.urls.defaults import *

urlpatterns = patterns('labgeeksrpg.people.views',
                       url(r'^(?P<name>\w+)/$', 'view_profile', name="People-View_Profile"),
                       url(r'^(?P<name>\w+)/edit/$', 'create_user_profile', name="People-Create_Profile"),
                       url(r'^(?P<user>\w+)/review/$', 'edit_reviews', name="People-Edit_Reviews"),
                       url(r'^(?P<user>\w+)/view_reviews/$', 'view_reviews', name="People-View_Reviews"),
                       url(r'^(?P<user>\w+)/view_reviews/info/$', 'view_review_data', name="People-View_Review_Data"),
                       url(r'^(?P<user>\w+)/wage_history/$', 'view_wage_history', name="People-Wage_History"),
                       (r'^$', 'list_all'),
                       )
