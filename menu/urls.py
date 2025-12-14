from django.urls import re_path
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified

from django.conf import settings

# from .views import (
#     IndexView, ProductView, CatalogView, latest_entry_menu,
#     import_image, set_slug, set_param_category
# )

# app_name = 'menu'

# urlpatterns = [
#     # URL de la page d'accueil (inchangée)
#     re_path(r'^$', cache_page(settings.CACHE_TIME_BASE_VIEW)(IndexView.as_view()), name='catalog_home'),

#     # URL pour les pages de détail des produits (inchangée)
#     re_path(r'^product/(?P<product_slug>[-\w]+)/$', ProductView.as_view(), name='product_detail'),

#     # URLs utilitaires (inchangées)
#     re_path(r'^import_image/([^/]*)/([^/]*)/([^*]*)/$', import_image, name='import_image'),
#     re_path(r'^set_slug/(\d+)/([^*]*)/$', set_slug, name='set_slug'),
#     re_path(r'^set_param/(\d+)/([^*]*)/$', set_param_category, name='set_param_category'),

#     # --- NOUVELLE LOGIQUE POUR LES CATALOGUES ---

#     # 1. NOUVELLE URL pour les catégories AVEC filtres (le format /f/...)
#     # Cette URL doit être placée AVANT les autres URLs de catalogue plus générales.
#     re_path(
#         r'^(?P<menu_slug>[-\w]+)/f/(?P<filters_str>.*)/$',
#         last_modified(latest_entry_menu)(cache_page(settings.CACHE_TIME_BASE_VIEW)(CatalogView.as_view())),
#         name='menu_catalog_filtered'
#     ),

#     # 2. ANCIENNE URL pour la compatibilité (ex: /categorie/marque/gost/)
#     # Cette URL capture tout ce qui n'est pas le nouveau format.
#     # On la renomme pour éviter les conflits.
#     re_path(
#         r'^(?P<menu_slug>[-\w]+)/.*/$',  # Accepte n'importe quoi après le slug
#         last_modified(latest_entry_menu)(cache_page(settings.CACHE_TIME_BASE_VIEW)(CatalogView.as_view())),
#         name='menu_catalog_legacy_params'
#     ),

#     # 3. URL de base pour une catégorie SANS filtres
#     # C'est la dernière, la plus générale.
#     re_path(
#         r'^(?P<menu_slug>[-\w]+)/$',
#         last_modified(latest_entry_menu)(cache_page(settings.CACHE_TIME_BASE_VIEW)(CatalogView.as_view())),
#         name='menu_catalog_detail'
#     ),
# ]


from .views import (
    IndexView, ProductView, CatalogView, latest_entry_menu,
    import_image, set_slug, set_param_category
)



# --- IMPORTS AJOUTÉS DEPUIS URLS_FORM.PY ---
from .views_form import CartCountView, SendFormOrder, GetFilterUrl

app_name = 'menu' # Le seul et unique namespace pour cette application

# urlpatterns = [
#     # URL de la page d'accueil
#     # re_path(r'^$', cache_page(settings.CACHE_TIME_BASE_VIEW)(IndexView.as_view()), name='catalog_home'),

#     re_path(r'^$', IndexView.as_view(), name='catalog_home'),


#     # --- URLS AJOUTÉES DEPUIS URLS_FORM.PY ---
#     re_path(r'^get_cart_count$', CartCountView.as_view(), name='get_cart_count'),
#     re_path(r'^get_filter_url$', GetFilterUrl.as_view(), name='get_filter_url'), # J'ai ajouté un '$' pour la cohérence
#     re_path(r'^send_form_order$', SendFormOrder.as_view(), name='send_form_order'),
    
#     # URL pour les pages de détail des produits
#     re_path(r'^product/(?P<product_slug>[-\w]+)/$', ProductView.as_view(), name='product_detail'),

#     # URLs utilitaires
#     re_path(r'^import_image/([^/]*)/([^/]*)/([^*]*)/$', import_image, name='import_image'),
#     re_path(r'^set_slug/(\d+)/([^*]*)/$', set_slug, name='set_slug'),
#     re_path(r'^set_param/(\d+)/([^*]*)/$', set_param_category, name='set_param_category'),

#     # --- URLs de catalogue que nous avons modernisées ---
#     re_path(
#         r'^(?P<menu_slug>[-\w]+)/f/(?P<filters_str>.*)/$',
#         last_modified(latest_entry_menu)(CatalogView.as_view()), # J'ai enlevé le cache pour le débogage
#         name='menu_catalog_filtered'
#     ),
#     re_path(
#         r'^(?P<menu_slug>[-\w]+)/$',
#         last_modified(latest_entry_menu)(CatalogView.as_view()),
#         name='menu_catalog_detail'
#     ),
# ]


urlpatterns = [
    # URL de la page d'accueil
    re_path(r'^$', IndexView.as_view(), name='catalog_home'),

    # --- URLS AJOUTÉES DEPUIS URLS_FORM.PY ---
    re_path(r'^get_cart_count$', CartCountView.as_view(), name='get_cart_count'),
    re_path(r'^get_filter_url$', GetFilterUrl.as_view(), name='get_filter_url'),
    re_path(r'^send_form_order$', SendFormOrder.as_view(), name='send_form_order'),
    
    # URL pour les pages de détail des produits
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', ProductView.as_view(), name='product_detail'),

    # URLs utilitaires (gardées pour la compatibilité, si elles sont encore utilisées)
    re_path(r'^import_image/([^/]*)/([^/]*)/([^*]*)/$', import_image, name='import_image'),
    re_path(r'^set_slug/(\d+)/([^*]*)/$', set_slug, name='set_slug'),
    re_path(r'^set_param/(\d+)/([^*]*)/$', set_param_category, name='set_param_category'),

    # --- NOUVELLE HIÉRARCHIE D'URLS POUR LE CATALOGUE ---

    # Règle 1 : La plus spécifique -> Catégorie + Filtres + Pagination
    re_path(
        r'^(?P<menu_slug>[-\w]+)/f/(?P<filters_str>.*)/page/(?P<page>\d+)/$',
        last_modified(latest_entry_menu)(CatalogView.as_view()),
        name='menu_catalog_filtered_paginated'
    ),
    
    # Règle 2 : Catégorie + Filtres (sans pagination)
    re_path(
        r'^(?P<menu_slug>[-\w]+)/f/(?P<filters_str>.*)/$',
        last_modified(latest_entry_menu)(CatalogView.as_view()),
        name='menu_catalog_filtered'
    ),
    
    # Règle 3 : Catégorie + Pagination (sans filtres)
    re_path(
        r'^(?P<menu_slug>[-\w]+)/page/(?P<page>\d+)/$',
        last_modified(latest_entry_menu)(CatalogView.as_view()),
        name='menu_catalog_paginated'
    ),

    # Règle 4 : La plus générale -> Catégorie seule
    re_path(
        r'^(?P<menu_slug>[-\w]+)/$',
        last_modified(latest_entry_menu)(CatalogView.as_view()),
        name='menu_catalog_detail'
    ),
]