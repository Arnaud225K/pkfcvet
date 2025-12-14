# -*- coding: utf-8 -*-
from django.contrib import admin

from import_control.models import ImportControl


class ImportControlAdmin(admin.ModelAdmin):
    """
    Настройка админки для Menu.
    """
    search_fields = ('slug', 'dublicate_id','original_id')
    list_display = ('slug', 'date', 'dublicate_id', 'original_id', 'slug', 'info', 'result')


admin.site.register(ImportControl, ImportControlAdmin)

