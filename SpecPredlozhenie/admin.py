# -*- coding: utf-8 -*-
from django.contrib import admin

from SpecPredlozhenie.models import SpecPredlozhenie

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class SpecPredlozhenieMenuAdmin(admin.ModelAdmin):
	list_display = ('name','text')

admin.site.register(SpecPredlozhenie,SpecPredlozhenieMenuAdmin)
