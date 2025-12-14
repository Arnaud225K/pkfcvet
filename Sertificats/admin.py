# -*- coding: utf-8 -*-
from django.contrib import admin

from Sertificats.models import SertificatsGroup, Sertificats
class SertificatsAdmin(admin.ModelAdmin):
    list_display = ('name','order_number', 'group', 'title_main',)

admin.site.register(SertificatsGroup)
admin.site.register(Sertificats, SertificatsAdmin)