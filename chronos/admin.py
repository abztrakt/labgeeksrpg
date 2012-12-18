from labgeeksrpg.chronos.models import *
from django.contrib import admin


class ShiftAdmin(admin.ModelAdmin):
    list_filter = ('person',)
    search_fields = ['person', 'shiftnote']
admin.site.register(Shift, ShiftAdmin)

admin.site.register(Location)
admin.site.register(Punchclock)
