from django.contrib import admin
from labgeeksrpg.wiki.models import Page


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Page, PageAdmin)
