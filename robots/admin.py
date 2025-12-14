# -*- coding: utf-8 -*-
from django.contrib import admin

from robots.models import RobotsTxt


class RobotsAdmin(admin.ModelAdmin):
    list_display = ('filial', 'text')

admin.site.register(RobotsTxt, RobotsAdmin)
