from django.contrib import admin
from search.models import SearchTerm, SearchChange, SearchRemove


class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('q', 'q_change', 'search_date', 'ip_address', 'path_site', 'filial_name')
    search_fields = ('ip_address', 'q')
    exclude = ('user',)

admin.site.register(SearchTerm, SearchTermAdmin)


class SearchChangeAdmin(admin.ModelAdmin):
    search_fields = ('source', 'result')
    list_display = ('source', 'result')

admin.site.register(SearchChange, SearchChangeAdmin)
admin.site.register(SearchRemove)