# from menu.models import MenuCatalog, Product, tableProductDop, ProductUsluga
# from django.contrib import admin


# class MenuAdmin(admin.ModelAdmin):
#     """
#     Настройка админки для Menu.
#     """
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('id', 'name', 'parent__name')
#     list_display = ('id', 'name', 'slug','parent', 'typeMenu', 'isHidden', 'created_at', 'updated_at')
#     list_filter = ('typeMenu',)


# admin.site.register(MenuCatalog, MenuAdmin)


# class ProductAdmin(admin.ModelAdmin):
#     """
#     Настройка админки для Menu.
#     """
#     list_display = ('id', 'name_main', 'slug',)
#     list_filter = ('catalog',)
#     search_fields = ('id', 'name_main', 'marka__name', 'gost__name', 'slug')


# admin.site.register(Product, ProductAdmin)

# admin.site.register(tableProductDop)
# admin.site.register(ProductUsluga)


# menu/admin.py

from django.contrib import admin
from .models import MenuCatalog, Product, tableProductDop, ProductUsluga

@admin.register(MenuCatalog)
class MenuAdmin(admin.ModelAdmin):
    """
    Configuration avancée pour le modèle MenuCatalog.
    """
    list_display = (
        'id', 
        'name', 
        'parent', 
        'typeMenu', 
        'isHidden', 
        'product_count',
        'updated_at'
    )
    list_display_links = ('id', 'name')
    list_filter = ('typeMenu', 'isHidden')
    list_select_related = ('parent', 'typeMenu')
    list_per_page = 25 

    search_fields = ('id', 'name', 'slug', 'parent__name')

    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations Générales', {
            'fields': ('name', 'slug', 'parent', 'typeMenu')
        }),
        ('Contenu & SEO', {
            'fields': ('description', 'title_main', 'keywords', 'keywords_description')
        }),
        ('Affichage & Options', {
            'classes': ('collapse',),
            'fields': ('isHidden', 'order_number', 'image')
        }),
        ('Dates (non modifiables)', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Nombre de Produits'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuration avancée pour le modèle Product.
    """
    list_display = (
        'id', 
        'name_main', 
        'catalog', 
        'price',
        'marka', 
        'gost', 
        'isHidden', 
        'updated_at'
    )
    list_display_links = ('id', 'name_main')
    list_filter = ('isHidden',)
    list_select_related = ('catalog', 'marka', 'gost')
    list_per_page = 25

    search_fields = ('id', 'name_main', 'slug', 'marka__name', 'gost__number')
    autocomplete_fields = ['catalog', 'marka', 'gost']

    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Produit', {
            'fields': ('name_main', 'slug', 'catalog', ('marka', 'gost'))
        }),
        ('Détails & Spécifications', {
            'fields': ('price', 'ed_izm', ('size_a', 'size_b', 'size_c'), 'description')
        }),
        ('Médias & Affichage', {
            'classes': ('collapse',),
            'fields': ('image', 'isHidden', 'order_number')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('title_main', 'keywords', 'keywords_description')
        }),
        ('Date', {
            'fields': ('updated_at',),
        }),
    )
    
@admin.register(tableProductDop)
class TableProductDopAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    search_fields = ('product__name_main',)
    autocomplete_fields = ['product']

@admin.register(ProductUsluga)
class ProductUslugaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    search_fields = ('product__name_main',)
    autocomplete_fields = ['product']