# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from GOST.models import GOSTHead, GOSTGroup, GOST

from headers import ID_MENU_GOST

import datetime

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class SitemapGOSTHeadXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.5

    def items(self):
        return GOSTHead.objects.filter(isHidden=False).order_by('id')

    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return "/gost/"+str(ID_MENU_GOST)+"/%s/" % obj.id

class SitemapGOSTXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.5

    def items(self):
        return GOSTGroup.objects.filter(isHidden=False).order_by('id')


    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return "/gost/"+str(ID_MENU_GOST)+"/"+str(obj.position.id)+"/"+str(obj.id)

class SitemapOneGOSTXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.8

    def items(self):
        return GOST.objects.filter(isHidden=False).order_by('id')


    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return "/gost/"+str(ID_MENU_GOST)+"/"+str(obj.position.position.id)+"/"+str(obj.position.id)+"/"+str(obj.id)