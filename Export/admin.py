# -*- coding: utf-8 -*-
from django.contrib import admin

from Export.models import ExportExcel

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


#class TextBlockMainMenuAdmin(admin.ModelAdmin):
#	list_filter = ('position',)

admin.site.register(ExportExcel)





#admin.site.register(ExportExcel)

