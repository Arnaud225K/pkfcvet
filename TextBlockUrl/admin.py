# -*- coding: utf-8 -*-
from django.contrib import admin

from TextBlockUrl.models import TextBlockUrl


class TextBlockUrlAdmin(admin.ModelAdmin):
    search_fields = ('name', 'url')
    list_display = ('name', 'url', 'filial')


admin.site.register(TextBlockUrl, TextBlockUrlAdmin)
