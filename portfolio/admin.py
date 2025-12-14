# -*- coding: utf-8 -*-
from django.contrib import admin

from portfolio.models import Portfolio

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class PortfolioAdmin(admin.ModelAdmin):
	list_display = ('name','text')

admin.site.register(Portfolio,PortfolioAdmin)
