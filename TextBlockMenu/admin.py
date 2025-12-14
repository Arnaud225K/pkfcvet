# -*- coding: utf-8 -*-
from django.contrib import admin

from TextBlockMenu.models import TextBlockMenu


class TextBlockMenuAdmin(admin.ModelAdmin):
    list_display = ('name','position')
    list_filter = ('position',)


admin.site.register(TextBlockMenu,TextBlockMenuAdmin)
