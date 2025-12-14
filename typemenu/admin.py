from django.contrib import admin

from typemenu.models import TypeMenu

# admin.site.register(TypeMenu)


@admin.register(TypeMenu)
class TypeMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template')
    search_fields = ('name',)
    
    # readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'template')
        }),
        # ("Информация о записи", {
        #     'classes': ('collapse',),
        #     'fields': ('created_at', 'updated_at')
        # }),
    )
