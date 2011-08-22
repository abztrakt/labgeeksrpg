from labgeeksrpg.people.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(EmploymentStatus)
admin.site.register(TimePeriod)
admin.site.register(WorkGroup)
admin.site.register(PayGrade)
admin.site.register(Title)
admin.site.register(UserProfile)

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
