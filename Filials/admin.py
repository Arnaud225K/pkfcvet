# -*- coding: utf-8 -*-
from django.contrib import admin

from Filials.models import Filials


class FilialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain_name', 'phone', 'email', 'phone_dop',)


admin.site.register(Filials, FilialsAdmin)
