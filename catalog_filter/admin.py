from django.contrib import admin

from catalog_filter.models import CatalogFilterName, CatalogFilterValue


@admin.register(CatalogFilterName)
class CatalogFilterNameAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name_lat')
    list_display = ('name', 'name_lat')


@admin.register(CatalogFilterValue)
class CatalogFilterValueAdmin(admin.ModelAdmin):
    list_filter = ('filter_name',)
    
    search_fields = (
        'value', 
        'value_lat', 
        'category__name', 
        'filter_name__name'
    )
    
    list_display = ('category__name', 'filter_name', 'value', 'value_lat')
    
    list_display_links = ('value',)
    
    autocomplete_fields = ('category', 'filter_name')
