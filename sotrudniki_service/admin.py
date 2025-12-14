# -*- coding: utf-8 -*-
from django.contrib import admin

from sotrudniki_service.models import SotrudnikiService


class SotrudnikiServiceAdmin(admin.ModelAdmin):
    list_display = ('name','position')
    list_filter = ('position',)


admin.site.register(SotrudnikiService,SotrudnikiServiceAdmin)
