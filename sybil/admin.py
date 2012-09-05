from django.contrib import admin
from labgeeksrpg.sybil.models import Screenshot


class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date', )
    readonly_fields = ('user', 'date', )

admin.site.register(Screenshot, ScreenshotAdmin)
