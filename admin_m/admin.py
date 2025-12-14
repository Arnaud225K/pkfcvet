from django.contrib import admin
from .models import ImportData, StateData, ExportData


class ImportDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user', 'email', 'action', 'state', 'result', 'file')
    list_filter = ('state',)
    search_fields = ('email', 'name', 'user', 'id')


class ExportDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user', 'email', 'state', 'result', 'info', 'link')
    list_filter = ('state',)
    search_fields = ('email', 'name', 'user', 'id')


admin.site.register(ExportData, ExportDataAdmin)
admin.site.register(ImportData, ImportDataAdmin)
admin.site.register(StateData)
