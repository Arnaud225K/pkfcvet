# -*- coding: utf-8 -*-
from django.contrib import admin

from videogallery.models import Videogallery
class PhotogalleryAdmin(admin.ModelAdmin):
    list_display = ('name','order_number', 'url')

admin.site.register(Videogallery, PhotogalleryAdmin)