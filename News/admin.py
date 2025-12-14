# -*- coding: utf-8 -*-
from django.contrib import admin

from News.models import News, NewsType

admin.site.register(NewsType)
admin.site.register(News)