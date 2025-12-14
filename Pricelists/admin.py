# -*- coding: utf-8 -*-
from django.contrib import admin

from Pricelists.models import Pricelists, PricelistsMain


class PricelistsAdmin(admin.ModelAdmin):
    list_display = ('name','order_number', 'date')

admin.site.register(Pricelists, PricelistsAdmin)

class PricelistsMainAdmin(admin.ModelAdmin):
    list_display = ('name','order_number', 'date')

admin.site.register(PricelistsMain, PricelistsMainAdmin)