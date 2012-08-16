from labgeeksrpg.schedule.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(BaseShift)
admin.site.register(ShiftType)
admin.site.register(DefaultShift)
admin.site.register(WorkShift)
admin.site.register(TimePeriod)
