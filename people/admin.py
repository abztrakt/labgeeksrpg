from labgeeksrpg.people.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class EmploymentStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(EmploymentStatus, EmploymentStatusAdmin)

class TimePeriodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(TimePeriod, TimePeriodAdmin)

class WorkGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(WorkGroup, WorkGroupAdmin)

class PayGradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(PayGrade, PayGradeAdmin)

class TitleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Title, TitleAdmin)
admin.site.register(UserProfile)

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
