# -*- coding: utf-8 -*-
from django.contrib import admin

from GOST.models import GOSTHead, GOSTGroup, GOST

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class GOSTGroupAdmin(admin.ModelAdmin):
    list_filter = ('position',)
    list_display = ('name','number','position','order_number')

class GOSTAdmin(admin.ModelAdmin):
    list_filter = ('position',)
    list_display = ('name','number','number_lat','position','order_number','description')
    search_fields = ('name','number','number_lat',)

admin.site.register(GOSTHead)
admin.site.register(GOSTGroup,GOSTGroupAdmin)
admin.site.register(GOST,GOSTAdmin)

