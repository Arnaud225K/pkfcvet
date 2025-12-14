# -*- coding: utf-8 -*-
from django.contrib import admin

from Marochnik.models import Metall, MetallGroup, MarkaMetall

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class MetallGroupAdmin(admin.ModelAdmin):
    list_filter = ('position',)

class MarkaMetallAdmin(admin.ModelAdmin):
    list_filter = ('position',)
    list_display = ('name', 'name_lat',)
    search_fields = ('name', 'name_lat',)

admin.site.register(Metall)
admin.site.register(MetallGroup, MetallGroupAdmin)
admin.site.register(MarkaMetall, MarkaMetallAdmin)
