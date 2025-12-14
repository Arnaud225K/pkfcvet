# -*- coding: utf-8 -*-
from django.contrib import admin

from photogallery.models import PhotogalleryGroup, Photogallery
class PhotogalleryAdmin(admin.ModelAdmin):
    list_display = ('name','order_number', 'group', 'title_main',)

admin.site.register(PhotogalleryGroup)
admin.site.register(Photogallery, PhotogalleryAdmin)