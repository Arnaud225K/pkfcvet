import os
import time
import re
import json
from datetime import datetime
from operator import itemgetter
from itertools import groupby
from django.core import serializers

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotModified, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from django.conf import settings
from django.db.models import Prefetch, Q

# Imports pour les requêtes HTTP en Python 3
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from PIL import Image
from transliterate import translit
from django.utils.http import parse_http_date_safe
from email.utils import formatdate
from django.db.models import Count



# Imports des modèles (regroupés et propres)
from .models import MenuCatalog, Product
from TextBlockMenu.models import TextBlockMenu
from slider.models import Slider
from News.models import News
from SpecPredlozhenie.models import SpecPredlozhenie
from portfolio.models import Portfolio
from Marochnik.models import MarkaMetall, Metall
from GOST.models import GOST
from Partners.models import Partners
from advanteges.models import Advanteges
from manufactures.models import Manufactures
from awards.models import Awards
from vacancy.models import Vacancy
from Sertificats.models import Sertificats
from sotrudniki_service.models import SotrudnikiService
from Pricelists.models import Pricelists
from TextBlockUrl.models import TextBlockUrl
from catalog_filter.models import CatalogFilterValue, CatalogFilterName
from cart import cartpy
from .views_form import get_current_filial # On suppose que c'est le bon chemin



CONTROL_CODE = "73aoF6N"
SIZE_PAGE = 20



def datetime2rfc(updated_at):
    """Convertit un objet datetime en une chaîne de caractères au format RFC 2822."""
    dt_timestamp = time.mktime(updated_at.timetuple())
    return formatdate(dt_timestamp, usegmt=True)

def _if_modified_since(date_server_str, last_modified_str):
    """Compare deux dates au format HTTP pour la gestion du cache."""
    try:
        last_modified_dt = parse_http_date_safe(last_modified_str)
        date_server_dt = parse_http_date_safe(date_server_str)
        if last_modified_dt is not None and date_server_dt is not None:
            return date_server_dt <= last_modified_dt
    except (TypeError, ValueError):
        pass
    return False

def handle_uploaded_file(f, file_name):
    """Sauvegarde un fichier uploadé dans le dossier media."""
    filename = os.path.join(settings.MEDIA_ROOT, file_name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def key_sort(item):
    """
    Fonction de tri robuste pour les listes contenant des nombres, des chaînes et None.
    Attend un dictionnaire en entrée, ex: {'size_a': '10'}.
    """
    val = list(item.values())[0]

    if val is None:
        return (2, float('inf')) 
    
    try:
        numeric_val = float(str(val).replace(',', '.'))
        return (0, numeric_val)
    except (ValueError, TypeError):
        return (1, str(val))

def get_filter_list(select_type, s1, s2, s3, s4, s5, s6, s7, marka, gost, size_x):
    """
    Récupère une liste de valeurs de filtre distinctes basées sur les filtres actuels.
    (La logique reste la même pour l'instant, mais les requêtes sont corrigées pour Python 3)
    """
    all_products = Product.objects.filter(catalog=select_type, isHidden=False)
    all_products |= Product.objects.filter(catalogOne=select_type, isHidden=False)
    all_products |= Product.objects.filter(catalogTwo=select_type, isHidden=False)
    all_products |= Product.objects.filter(catalogThree=select_type, isHidden=False)
    if marka:
        all_products = all_products.filter(marka__name_lat__iexact=marka)
    if gost:
        all_products = all_products.filter(gost__number_lat__iexact=gost)
    if s1: all_products = all_products.filter(size_a=s1)
    if s2: all_products = all_products.filter(size_b=s2)
    if s3: all_products = all_products.filter(size_c=s3)
    if s4: all_products = all_products.filter(size_d=s4)
    if s5: all_products = all_products.filter(size_e=s5)
    if s6: all_products = all_products.filter(size_f=s6)
    if s7: all_products = all_products.filter(size_l=s7)

    if size_x == 'marka__name' or size_x == 'gost__number':
        sx_filter = all_products.values(size_x, size_x+'_lat').distinct().order_by(size_x)
        if sx_filter and list(sx_filter[0].values()) and not list(sx_filter[0].values())[0]:
            sx_filter = sx_filter[1:]
    else:
        sx_filter = all_products.values(size_x).distinct().order_by(size_x)
        if sx_filter and list(sx_filter[0].values()) and not list(sx_filter[0].values())[0]:
            sx_filter = sx_filter[1:]

    if sx_filter and list(sx_filter[0].values()) and list(sx_filter[0].values())[0]:
        return sorted(sx_filter, key=key_sort)
    else:
        return None



def latest_entry_menu(request, *args, **kwargs):
    menu_slug = kwargs.get('menu_slug')
    if not menu_slug:
        return None

    try:
        current_menu = MenuCatalog.objects.only('updated_at').get(slug__iexact=menu_slug)
        return current_menu.updated_at
    except MenuCatalog.DoesNotExist:
        return datetime.now()


# class IndexView(TemplateView):
#     template_name = "catalog/index.html"

#     def get(self, request):
#         request.session.clear_expired()
        
#         sliders = Slider.objects.filter(isHidden=False)
#         specpredlozh_list = SpecPredlozhenie.objects.filter(isShowMain=True, isHidden=False)
#         portfolio_list = Portfolio.objects.filter(isShowMain=True, isHidden=False)
#         news_list = News.objects.filter(isMain=True, isHidden=False).order_by("-date")[:2]
#         partners_list = Partners.objects.filter(isMain=True, isHidden=False)
#         advanteges_list = Advanteges.objects.filter(isMain=True, isHidden=False)
        
#         current_filial = get_current_filial(request.get_host())
        
#         dop_text_block_url = TextBlockUrl.objects.filter(
#             Q(url="/", filial=current_filial, isHidden=False) | 
#             Q(url="/", filial__isnull=True, isHidden=False)
#         ).first()

#         current_menu = get_object_or_404(MenuCatalog.objects.select_related('typeMenu'), id=1)
#         current_menu_catalog = get_object_or_404(MenuCatalog.objects.select_related('typeMenu'), id=2)
#         text_blocks_menu = TextBlockMenu.objects.filter(position__name="Главная").first()
        
#         context = {
#             'products_featured': [],
#             'products_men': [],
#             'products_women': [],
#             'page_title': 'Главная',
#             'sliders': sliders,
#             'specpredlozh_list': specpredlozh_list,
#             'portfolio_list': portfolio_list,
#             'news_list': news_list,
#             'partners_list': partners_list,
#             'advanteges_list': advanteges_list,
#             'current_filial': current_filial,
#             'dop_text_block_url': dop_text_block_url,
#             'current_menu': current_menu,
#             'current_menu_catalog': current_menu_catalog,
#             'text_blocks_menu': text_blocks_menu,
#         }
#         return render(request, self.template_name, context)


class IndexView(TemplateView):
    """
    Affiche la page d'accueil avec des données pré-chargées pour la performance.
    """
    template_name = "catalog/index.html"

    def get(self, request, *args, **kwargs):
        # Nettoyage des sessions expirées
        request.session.clear_expired()


        # 1. Pré-charger les menus et leurs descendants (2 niveaux)
        main_menus_catalog = MenuCatalog.objects.filter(
            Q(parent=None, comment="", typeMenu__name="Каталог", isHidden=False) |
            Q(parent=None, comment="", name="Производство", isHidden=False)
        ).prefetch_related(
            # Pré-charger les enfants (niveau 1) et stocker dans 'child_menus'
            Prefetch(
                'menucatalog_set',
                queryset=MenuCatalog.objects.filter(isHidden=False).only('name', 'slug', 'image'),
                to_attr='child_menus'
            )
        )[:5]

        # --- NOUVELLE LOGIQUE : Pré-charger les petits-enfants séparément ---
        # C'est une méthode plus robuste que le prefetch imbriqué direct

        # D'abord, on récupère les IDs de tous les enfants qui seront affichés
        child_ids = []
        for menu in main_menus_catalog:
            child_ids.extend([child.id for child in menu.child_menus])

        # Ensuite, on récupère tous les petits-enfants en une seule requête
        children_with_grandchildren = MenuCatalog.objects.filter(
            id__in=child_ids
        ).prefetch_related(
            Prefetch(
                'menucatalog_set',
                queryset=MenuCatalog.objects.filter(isHidden=False).only('name', 'slug'),
                to_attr='child_sub_menus' # On stocke les petits-enfants ici
            )
        )
        
        # On crée un dictionnaire pour retrouver facilement les enfants par leur ID
        children_map = {child.id: child for child in children_with_grandchildren}

        # Enfin, on attache les petits-enfants pré-chargés aux bons enfants
        for menu in main_menus_catalog:
            for child in menu.child_menus:
                if child.id in children_map:
                    # On remplace l'objet enfant par celui qui contient les petits-enfants
                    child.child_sub_menus = children_map[child.id].child_sub_menus
                else:
                    # Au cas où, pour éviter une erreur
                    child.child_sub_menus = []

        sliders = Slider.objects.filter(isHidden=False)
        specpredlozh_list = SpecPredlozhenie.objects.filter(isShowMain=True, isHidden=False)
        portfolio_list = Portfolio.objects.filter(isShowMain=True, isHidden=False)
        news_list = News.objects.filter(isMain=True, isHidden=False).order_by("-date")[:2]
        partners_list = Partners.objects.filter(isMain=True, isHidden=False)
        advanteges_list = Advanteges.objects.filter(isMain=True, isHidden=False)
        
        # 3. Données liées à la requête (filiale, bloc de texte)
        current_filial = get_current_filial(request.get_host())
        
        dop_text_block_url = TextBlockUrl.objects.filter(
            Q(url="/", filial=current_filial, isHidden=False) | 
            Q(url="/", filial__isnull=True, isHidden=False)
        ).order_by('-filial').first() # Priorise le bloc spécifique à la filiale

        # 4. Objets uniques pour la page
        # Utiliser get_object_or_404 garantit que ces objets existent
        try:
            # On utilise .filter().first() pour éviter de crasher si l'ID n'existe pas
            current_menu = MenuCatalog.objects.filter(id=1).select_related('typeMenu').first()
            current_menu_catalog = MenuCatalog.objects.filter(id=2).select_related('typeMenu').first()
            text_blocks_menu = TextBlockMenu.objects.filter(position__name="Главная").first()
        except MenuCatalog.DoesNotExist:
            current_menu, current_menu_catalog = None, None
        except TextBlockMenu.DoesNotExist:
            text_blocks_menu = None


        # --- CONSTRUCTION DU CONTEXTE EXPLICITE ---
        
        context = {
            'page_title': 'Главная',
            'main_menus_catalog': main_menus_catalog,
            'sliders': sliders,
            'specpredlozh_list': specpredlozh_list,
            'portfolio_list': portfolio_list,
            'news_list': news_list,
            'partners_list': partners_list,
            'advanteges_list': advanteges_list,
            'current_filial': current_filial,
            'dop_text_block_url': dop_text_block_url,
            'current_menu': current_menu,
            'current_menu_catalog': current_menu_catalog,
            'text_blocks_menu': text_blocks_menu,
        }
        
        return render(request, self.template_name, context)


# class CatalogView(TemplateView):
#     template_name = "catalog/category.html"

#     def _parse_filters_from_url(self, current_menu, **kwargs):
#         """
#         Parse les filtres DEPUIS L'URL. Ne retourne que les SLUGS (_lat).
#         """
#         filters = {
#             'marka_lat': None, 'current_marka': None,
#             'gost_lat': None, 'current_gost': None,
#             'page': 1,
#             's1_lat': None, 's2_lat': None, 's3_lat': None, 's4_lat': None,
#             's5_lat': None, 's6_lat': None, 's7_lat': None,
#         }
#         filters_str = kwargs.get('filters_str')
#         if not filters_str: return filters

#         url_key_map = { (getattr(current_menu, f'labelSize{s}slug') or f's{i}').lower(): f's{i}' for i, s in enumerate("ABCDEFL", 1) }

#         for part in filters_str.strip('/').split('/'):
#             try:
#                 key, value_lat = part.split('=', 1)
#                 key = key.lower()

#                 if key == 'marka':
#                     filters['marka_lat'] = value_lat
#                     filters['current_marka'] = MarkaMetall.objects.filter(name_lat__iexact=value_lat).first()
#                 elif key == 'gost':
#                     filters['gost_lat'] = value_lat
#                     filters['current_gost'] = GOST.objects.filter(number_lat__iexact=value_lat).first()
#                 elif key == 'page':
#                     filters['page'] = int(value_lat)
#                 elif key in url_key_map:
#                     internal_key = url_key_map[key] # ex: 's1'
#                     filters[f'{internal_key}_lat'] = value_lat
#             except ValueError:
#                 pass
#         return filters

#     def _apply_filters_to_queryset(self, queryset, filters):
#         """
#         Applique les filtres en se basant sur les SLUGS (_lat).
#         """
#         if filters.get('marka_lat'):
#             queryset = queryset.filter(marka__name_lat__iexact=filters['marka_lat'])
#         if filters.get('gost_lat'):
#             queryset = queryset.filter(gost__number_lat__iexact=filters['gost_lat'])
        
#         # Traduction sX_lat vers size_Y
#         size_map = {'s1_lat': 'size_a', 's2_lat': 'size_b', 's3_lat': 'size_c', 's4_lat': 'size_d', 's5_lat': 'size_e', 's6_lat': 'size_f', 's7_lat': 'size_l'}
#         for lat_key, field_name in size_map.items():
#             if value := filters.get(lat_key):
#                 # Pour les tailles, on doit retrouver la valeur brute
#                 try:
#                     value_obj = CatalogFilterValue.objects.get(value_lat__iexact=value, filter_name__name_lat__iexact=field_name, category=queryset.model._meta.get_field('catalog').remote_field.model.objects.get(slug=queryset.model._meta.get_field('catalog').remote_field.model.objects.get(id=queryset.first().catalog_id).slug))
#                     queryset = queryset.filter(**{f'{field_name}__iexact': value_obj.value})
#                 except (CatalogFilterValue.DoesNotExist, CatalogFilterValue.MultipleObjectsReturned, AttributeError):
#                     # Si on ne trouve pas dans CatalogFilterValue, on tente un filtre direct (moins fiable)
#                     queryset = queryset.filter(**{f'{field_name}__iexact': value.replace('-', '.')})
#         return queryset

#     def get(self, request, *args, **kwargs):
#         menu_slug = kwargs.get('menu_slug')
#         current_menu = get_object_or_404(MenuCatalog.objects.select_related('typeMenu', 'parent'), slug__iexact=menu_slug)
        
#         if menu_slug != current_menu.slug:
#             return HttpResponsePermanentRedirect(current_menu.get_absolute_url())

#         # 1. Parser les filtres (ne contient que les _lat)
#         applied_filters = self._parse_filters_from_url(current_menu, **kwargs)
        
#         # 2. Construire le queryset de base
#         base_products_qs = self._get_base_product_queryset(current_menu)
        
#         # 3. Générer les options de filtres disponibles AVANT de filtrer les produits
#         # Pour les MARQUES disponibles
#         qs_for_marka = self._apply_filters_to_queryset(base_products_qs, {**applied_filters, 'marka_lat': None})
#         marka_filter_options = list(qs_for_marka.values('marka__name', 'marka__name_lat').order_by('marka__name').distinct())
        
#         # Pour les GOSTs disponibles
#         qs_for_gost = self._apply_filters_to_queryset(base_products_qs, {**applied_filters, 'gost_lat': None})
#         gost_filter_options = list(qs_for_gost.values('gost__number', 'gost__number_lat').order_by('gost__number').distinct())
        
#         # ... Répéter pour les tailles ...
#         s_filter_options = {}
#         size_map_rev = {'size_a': 's1_lat', 'size_b': 's2_lat', 'size_c': 's3_lat', 'size_d': 's4_lat', 'size_e': 's5_lat', 'size_f': 's6_lat', 'size_l': 's7_lat'}
#         for field, key in size_map_rev.items():
#             temp_filters = applied_filters.copy()
#             temp_filters[key] = None
#             qs = self._apply_filters_to_queryset(base_products_qs, temp_filters)
#             # Pour les tailles, on a besoin des slugs ET des valeurs humaines.
#             # On va chercher dans CatalogFilterValue qui fait le lien.
#             filter_name = field
#             s_filter_options[f"{key.replace('_lat', '')}_filter"] = list(CatalogFilterValue.objects.filter(filter_name__name_lat=filter_name, category=current_menu).values('value', 'value_lat').distinct())

#         # 4. Maintenant, on filtre les produits pour l'affichage final
#         filtered_products_qs = self._apply_filters_to_queryset(base_products_qs, applied_filters)
        
#         # 5. Pagination
#         paginator = Paginator(filtered_products_qs.select_related('gost', 'marka'), SIZE_PAGE)
#         page_obj = paginator.get_page(applied_filters['page'])
        
#         page_num = page_obj.number
#         paginator_min = max(page_num - 5, 1)
#         paginator_max = min(page_num + 5, paginator.num_pages)

#         # 5. Récupérer les données annexes pour le contexte (y compris les listes que vous avez mentionnées)
#         current_filial = get_current_filial(request.get_host())

#         dynamic_h1 = self._build_dynamic_h1(current_menu, applied_filters, current_filial)
        
#         dop_text_block_url = TextBlockUrl.objects.filter(
#             Q(url=request.path, filial=current_filial, isHidden=False) |
#             Q(url=request.path, filial__isnull=True, isHidden=False)
#         ).order_by('-filial').first()
        
#         current_menu_main = current_menu.get_parent_menu()
#         metall_categories_similar = current_menu.get_metall_categories_similar()
        
#         news_list = News.objects.filter(isHidden=False)
#         advanteges_list = Advanteges.objects.filter(isHidden=False)
#         manufactures_list = Manufactures.objects.filter(isHidden=False)
#         awards_list = Awards.objects.filter(isHidden=False)
#         vacancy_list = Vacancy.objects.filter(isHidden=False)
#         sertificats_list = Sertificats.objects.filter(isHidden=False)
#         pricelist_list = Pricelists.objects.filter(isHidden=False)
#         text_blocks_menu = TextBlockMenu.objects.filter(position=current_menu)

#         # 6. Construire le contexte final
#         context = {
#             'current_menu': current_menu,
#             'products': page_obj,
#             'marka_filter': marka_filter_options,
#             'gost_filter': gost_filter_options,
#             **s_filter_options,
#             **applied_filters,

#             'page_title': current_menu.title_main or current_menu.name,
#             'meta_keywords': current_menu.keywords,
#             'meta_description': current_menu.keywords_description,
            
#             'current_filial': current_filial,
#             'dop_text_block_url': dop_text_block_url,
#             'current_menu_main': current_menu_main,

#             'dynamic_h1': dynamic_h1,
            
#             'metall_categories_similar': metall_categories_similar,
            
#             'paginatorMin': paginator_min,
#             'paginatorMax': paginator_max,

#             # Ajout des listes au contexte
#             'news_list': news_list,
#             'advanteges_list': advanteges_list,
#             'manufactures_list': manufactures_list,
#             'awards_list': awards_list,
#             'vacancy_list': vacancy_list,
#             'sertificats_list': sertificats_list,
#             'pricelist_list': pricelist_list,
#             'text_blocks_menu': text_blocks_menu,
#         }
        
#         # Ajouter les filtres actifs au contexte
#         context.update(applied_filters)
        
#         # Ajouter les listes de filtres disponibles
#         context['marka_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], applied_filters['s3'], applied_filters['s4'], applied_filters['s5'], applied_filters['s6'], applied_filters['s7'], None, applied_filters['gost'], 'marka__name')
#         context['gost_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], applied_filters['s3'], applied_filters['s4'], applied_filters['s5'], applied_filters['s6'], applied_filters['s7'], applied_filters['marka'], None, 'gost__number')
#         context['s1_filter'] = get_filter_list(current_menu.id, None, applied_filters['s2'], applied_filters['s3'], applied_filters['s4'], applied_filters['s5'], applied_filters['s6'], applied_filters['s7'], applied_filters['marka'], applied_filters['gost'], 'size_a')
#         context['s2_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], None, applied_filters['s3'], applied_filters['s4'], applied_filters['s5'], applied_filters['s6'], applied_filters['s7'], applied_filters['marka'], applied_filters['gost'], 'size_b')
#         context['s3_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], None, applied_filters['s4'], applied_filters['s5'], applied_filters['s6'], applied_filters['s7'], applied_filters['marka'], applied_filters['gost'], 'size_c')
#         context['s4_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], applied_filters['s3'], None, applied_filters['s5'], applied_filters['s6'], applied_filters['s7'], applied_filters['marka'], applied_filters['gost'], 'size_d')
#         context['s5_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], applied_filters['s3'], applied_filters['s4'], None, applied_filters['s6'], applied_filters['s7'], applied_filters['marka'], applied_filters['gost'], 'size_e')
#         context['s6_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], applied_filters['s3'], applied_filters['s4'], applied_filters['s5'], None, applied_filters['s7'], applied_filters['marka'], applied_filters['gost'], 'size_f')
#         context['s7_filter'] = get_filter_list(current_menu.id, applied_filters['s1'], applied_filters['s2'], applied_filters['s3'], applied_filters['s4'], applied_filters['s5'], applied_filters['s6'], None, applied_filters['marka'], applied_filters['gost'], 'size_l')

#         self.template_name = current_menu.typeMenu.template

#         return render(request, self.template_name, context)


class CatalogView(TemplateView):
    template_name = "catalog/category.html"

    # --- MÉTHODES D'AIDE (HELPERS) ---

    def _get_base_product_queryset(self, current_menu):
        """Retourne le queryset de base pour les produits de la catégorie."""
        return Product.objects.filter(
            Q(catalog=current_menu) | Q(catalogOne=current_menu) |
            Q(catalogTwo=current_menu) | Q(catalogThree=current_menu),
            isHidden=False
        ).distinct()

    # def _parse_filters_from_url(self, current_menu, **kwargs):
    #     """
    #     Parse les filtres DEPUIS L'URL. Ne retourne que les SLUGS (_lat).
    #     """
    #     filters = {
    #         'marka_lat': None, 'current_marka': None,
    #         'gost_lat': None, 'current_gost': None,
    #         'page': 1,
    #         's1_lat': None, 's2_lat': None, 's3_lat': None, 's4_lat': None,
    #         's5_lat': None, 's6_lat': None, 's7_lat': None,
    #     }
    #     filters_str = kwargs.get('filters_str')
    #     if not filters_str:
    #         return filters

    #     # Création de la carte de correspondance (nom_url -> nom_interne)
    #     url_key_to_internal_map = {
    #         (getattr(current_menu, f'labelSize{s}slug') or f's{i}').lower(): f's{i}'
    #         for i, s in enumerate("ABCDEFL", 1)
    #     }

    #     for part in filters_str.strip('/').split('/'):
    #         try:
    #             key, value_lat = part.split('=', 1)
    #             key = key.lower()

    #             if key == 'marka':
    #                 filters['marka_lat'] = value_lat
    #                 filters['current_marka'] = MarkaMetall.objects.filter(name_lat__iexact=value_lat).first()
    #             elif key == 'gost':
    #                 filters['gost_lat'] = value_lat
    #                 filters['current_gost'] = GOST.objects.filter(number_lat__iexact=value_lat).first()
    #             elif key == 'page':
    #                 try:
    #                     filters['page'] = int(value_lat)
    #                 except (ValueError, TypeError):
    #                     filters['page'] = 1
    #             elif key in url_key_to_internal_map:
    #                 internal_key = url_key_to_internal_map[key]
    #                 filters[f'{internal_key}_lat'] = value_lat
    #         except ValueError:
    #             pass # Ignorer les parties malformées
    #     return filters

    def _parse_filters_from_url(self, current_menu, **kwargs):
        """
        Parse les filtres DEPUIS L'URL.
        Retourne les SLUGS (_lat) ET les valeurs HUMAINES pour l'affichage.
        """
        # 1. Initialiser toutes les clés dont le template aura besoin
        filters = {
            'marka': None, 'marka_lat': None, 'current_marka': None,
            'gost': None, 'gost_lat': None, 'current_gost': None,
            'page': 1,
            's1': "", 's1_lat': "", 's2': "", 's2_lat': "", 's3': "", 's3_lat': "",
            's4': "", 's4_lat': "", 's5': "", 's5_lat': "", 's6': "", 's6_lat': "",
            's7': "", 's7_lat': "",
        }
        
        filters_str = kwargs.get('filters_str')
        if not filters_str:
            return filters

        # 2. Création de la carte de correspondance (nom_url -> nom_interne)
        url_key_to_internal_map = {
            (getattr(current_menu, f'labelSize{s}slug') or f's{i}').lower(): f's{i}'
            for i, s in enumerate("ABCDEFL", 1)
        }

        # 3. Parsing de l'URL
        for part in filters_str.strip('/').split('/'):
            try:
                key, value_lat = part.split('=', 1)
                key = key.lower()

                if key == 'marka':
                    filters['marka_lat'] = value_lat
                    marka_obj = MarkaMetall.objects.filter(name_lat__iexact=value_lat).first()
                    if marka_obj:
                        filters['current_marka'] = marka_obj
                        filters['marka'] = marka_obj.name # <-- REMPLISSAGE DE LA VALEUR HUMAINE

                elif key == 'gost':
                    filters['gost_lat'] = value_lat
                    gost_obj = GOST.objects.filter(number_lat__iexact=value_lat).first()
                    if gost_obj:
                        filters['current_gost'] = gost_obj
                        filters['gost'] = gost_obj.number # <-- REMPLISSAGE DE LA VALEUR HUMAINE

                elif key == 'page':
                    try:
                        filters['page'] = int(value_lat)
                    except (ValueError, TypeError):
                        filters['page'] = 1

                elif key in url_key_to_internal_map:
                    internal_key = url_key_to_internal_map[key] # ex: 's1'
                    filters[f'{internal_key}_lat'] = value_lat
                    
                    # --- LA CORRECTION CLÉ EST ICI ---
                    # Traduction inverse pour trouver la valeur "humaine" de la taille
                    try:
                        filter_name_lat_map = {
                            's1': 'size_a', 's2': 'size_b', 's3': 'size_c', 's4': 'size_d',
                            's5': 'size_e', 's6': 'size_f', 's7': 'size_l'
                        }
                        filter_name_lat = filter_name_lat_map.get(internal_key)
                        
                        value_obj = CatalogFilterValue.objects.filter(
                            category=current_menu,
                            filter_name__name_lat__iexact=filter_name_lat,
                            value_lat__iexact=value_lat
                        ).first()
                        
                        if value_obj:
                            filters[internal_key] = value_obj.value # <-- REMPLISSAGE DE LA VALEUR HUMAINE
                        else:
                            filters[internal_key] = value_lat.replace('-', '.')
                    except Exception:
                        filters[internal_key] = value_lat.replace('-', '.')

            except ValueError:
                pass

        return filters

    def _apply_filters_to_queryset(self, queryset, filters):
        """
        Applique les filtres en se basant sur les SLUGS (_lat).
        """
        if filters.get('marka_lat'):
            queryset = queryset.filter(marka__name_lat__iexact=filters['marka_lat'])
        if filters.get('gost_lat'):
            queryset = queryset.filter(gost__number_lat__iexact=filters['gost_lat'])
        
        # Traduction sX_lat vers le champ de BDD size_Y
        size_map = {
            's1_lat': 'size_a', 's2_lat': 'size_b', 's3_lat': 'size_c', 's4_lat': 'size_d',
            's5_lat': 'size_e', 's6_lat': 'size_f', 's7_lat': 'size_l'
        }
        for lat_key, field_name in size_map.items():
            if value_lat := filters.get(lat_key):
                # Pour les tailles, on doit retrouver la valeur "humaine" car c'est ce qui est stocké
                # dans les champs size_a, size_b etc.
                try:
                    value_obj = CatalogFilterValue.objects.get(value_lat__iexact=value_lat, filter_name__name_lat__iexact=field_name, category=queryset.model._meta.get_field('catalog').remote_field.model.objects.get(id=queryset.first().catalog_id))
                    queryset = queryset.filter(**{f'{field_name}__iexact': value_obj.value})
                except (CatalogFilterValue.DoesNotExist, CatalogFilterValue.MultipleObjectsReturned, AttributeError):
                    # En cas d'échec, on tente un filtre direct sur la valeur slugifiée
                    queryset = queryset.filter(**{f'{field_name}__iexact': value_lat.replace('-', '.')})
        return queryset

    # def _build_dynamic_h1(self, current_menu, applied_filters, current_filial):
    #     """
    #     Construit le titre H1 dynamique en se basant sur les filtres appliqués.
    #     Version corrigée et robuste.
    #     """
    #     # 1. Commencer avec le nom de la catégorie
    #     parts = [current_menu.name]
        
    #     # 2. Ajouter les filtres principaux en utilisant les valeurs "humaines"
    #     if marka_name := applied_filters.get('marka'):
    #         parts.append(f"марка {marka_name}")
            
    #     if gost_number := applied_filters.get('gost'):
    #         parts.append(f"ГОСТ {gost_number}")

    #     # 3. Ajouter les filtres de taille, en utilisant les labels de la catégorie
    #     #    On s'assure de ne pas ajouter de label si la valeur est vide.
    #     size_parts = []
        
    #     # Carte de correspondance (clé de filtre -> champ de label dans MenuCatalog)
    #     size_map = {
    #         's1': 'labelSizeA', 's2': 'labelSizeB', 's3': 'labelSizeC', 's4': 'labelSizeD',
    #         's5': 'labelSizeE', 's6': 'labelSizeF', 's7': 'labelSizeL'
    #     }
        
    #     for size_key, label_attr in size_map.items():
    #         value = applied_filters.get(size_key)
    #         label = getattr(current_menu, label_attr, None)
            
    #         # Ajouter seulement si on a une valeur ET un label
    #         if value and label:
    #             size_parts.append(f"{label.lower()} {value}")
        
    #     if size_parts:
    #         parts.extend(size_parts)

    #     # 4. Joindre les parties avec un séparateur clair
    #     title = " ".join(parts)
        
    #     # 5. Ajouter la ville/filiale à la fin si nécessaire
    #     if current_filial and current_filial.name_p and current_filial.name != 'Екатеринбург':
    #         title += f" в {current_filial.name_p}"
            
    #     return title

    def _build_dynamic_h1(self, current_menu, applied_filters, current_filial, page_number=1):
        """
        Construit le titre H1 dynamique, en incluant le numéro de page si nécessaire.
        """
        # 1. Commencer avec le nom de la catégorie
        parts = [current_menu.name]
        
        # 2. Ajouter les filtres principaux
        if marka_name := applied_filters.get('marka'):
            parts.append(f"марка {marka_name}")
            
        if gost_number := applied_filters.get('gost'):
            parts.append(f"ГОСТ {gost_number}")

        # 3. Ajouter les filtres de taille
        size_parts = []
        size_map = {
            's1': 'labelSizeA', 's2': 'labelSizeB', 's3': 'labelSizeC', 's4': 'labelSizeD',
            's5': 'labelSizeE', 's6': 'labelSizeF', 's7': 'labelSizeL'
        }
        for size_key, label_attr in size_map.items():
            value = applied_filters.get(size_key)
            label = getattr(current_menu, label_attr, None)
            if value and label:
                size_parts.append(f"{label.lower()} {value}")
        if size_parts:
            parts.extend(size_parts)

        # 4. Joindre les parties
        title = " ".join(parts)
        
        # --- LA CORRECTION EST ICI ---
        # 5. Ajouter le numéro de page si ce n'est pas la première page
        try:
            # S'assurer que page_number est un entier
            page_num = int(page_number)
            if page_num > 1:
                title += f" — Страница {page_num}"
        except (ValueError, TypeError):
            pass # Ignorer si le numéro de page n'est pas un nombre valide

        # 6. Ajouter la ville/filiale à la fin
        if current_filial and current_filial.name_p and current_filial.name != 'Екатеринбург':
            title += f" в {current_filial.name_p}"
            
        return title

    # --- MÉTHODE GET PRINCIPALE ---

    # def get(self, request, *args, **kwargs):
    #     menu_slug = kwargs.get('menu_slug')
    #     current_menu = get_object_or_404(MenuCatalog.objects.select_related('typeMenu', 'parent'), slug__iexact=menu_slug)
        
    #     # Redirection SEO si la casse de l'URL n'est pas correcte
    #     if 'filters_str' not in kwargs and menu_slug != current_menu.slug:
    #         return HttpResponsePermanentRedirect(current_menu.get_absolute_url())

    #     # 1. Parser les filtres (ne contient que les _lat)
    #     applied_filters = self._parse_filters_from_url(current_menu, **kwargs)
        
    #     # 2. Construire le queryset de base
    #     base_products_qs = self._get_base_product_queryset(current_menu)
        
    #     # 3. Générer les options de filtres disponibles (logique à facettes)
    #     # Pour les MARQUES
    #     qs_for_marka = self._apply_filters_to_queryset(base_products_qs, {**applied_filters, 'marka_lat': None})
    #     marka_filter_options = list(qs_for_marka.values('marka__name', 'marka__name_lat').order_by('marka__name').distinct())
        
    #     # Pour les GOSTs
    #     qs_for_gost = self._apply_filters_to_queryset(base_products_qs, {**applied_filters, 'gost_lat': None})
    #     gost_filter_options = list(qs_for_gost.values('gost__number', 'gost__number_lat').order_by('gost__number').distinct())
        
    #     # Pour les TAILLES
    #     s_filter_options = {}
    #     size_map_rev = {'size_a': 's1_lat', 'size_b': 's2_lat', 'size_c': 's3_lat', 'size_d': 's4_lat', 'size_e': 's5_lat', 'size_f': 's6_lat', 'size_l': 's7_lat'}
    #     for field, key in size_map_rev.items():
    #         temp_filters = applied_filters.copy()
    #         temp_filters[key] = None
    #         qs_for_size = self._apply_filters_to_queryset(base_products_qs, temp_filters)
            
    #         # Récupérer les valeurs uniques et les slugs correspondants depuis CatalogFilterValue
    #         s_filter_options[f"{key.replace('_lat', '')}_filter"] = list(
    #             CatalogFilterValue.objects.filter(
    #                 filter_name__name_lat=field,
    #                 category=current_menu,
    #                 value__in=qs_for_size.values_list(field, flat=True).distinct()
    #             ).values('value', 'value_lat').distinct().order_by('value')
    #         )

    #     # 4. Maintenant, on filtre les produits pour l'affichage final
    #     filtered_products_qs = self._apply_filters_to_queryset(base_products_qs, applied_filters)


    #     current_filial = get_current_filial(request.get_host())
    #     dynamic_h1 = self._build_dynamic_h1(current_menu, applied_filters, current_filial)
        
    #     # 5. Pagination
    #     paginator = Paginator(filtered_products_qs.select_related('gost', 'marka'), SIZE_PAGE)
    #     page_obj = paginator.get_page(applied_filters['page'])
        
    #     page_num = page_obj.number
    #     paginator_min = max(page_num - 5, 1)
    #     paginator_max = min(page_num + 5, paginator.num_pages)

    #     # 6. Récupérer les données annexes
    #     current_filial = get_current_filial(request.get_host())
    #     dop_text_block_url = TextBlockUrl.objects.filter(Q(url=request.path, filial=current_filial, isHidden=False) | Q(url=request.path, filial__isnull=True, isHidden=False)).order_by('-filial').first()
    #     current_menu_main = current_menu.get_parent_menu()
    #     metall_categories_similar = current_menu.get_metall_categories_similar()
    #     news_list = News.objects.filter(isHidden=False)
    #     advanteges_list = Advanteges.objects.filter(isHidden=False)
    #     manufactures_list = Manufactures.objects.filter(isHidden=False)
    #     awards_list = Awards.objects.filter(isHidden=False)
    #     vacancy_list = Vacancy.objects.filter(isHidden=False)
    #     sertificats_list = Sertificats.objects.filter(isHidden=False)
    #     pricelist_list = Pricelists.objects.filter(isHidden=False)
    #     text_blocks_menu = TextBlockMenu.objects.filter(position=current_menu)

    #     # 7. Construire le contexte
    #     context = {
    #         'current_menu': current_menu,
    #         'products': page_obj,
    #         'marka_filter_list': page_obj,
    #         'marka_filter': marka_filter_options,
    #         'gost_filter': gost_filter_options,
    #         'paginatorMin': paginator_min,
    #         'paginatorMax': paginator_max,
    #         'dynamic_h1': dynamic_h1,
    #         # Données annexes
    #         'current_filial': current_filial,
    #         'dop_text_block_url': dop_text_block_url,
    #         'current_menu_main': current_menu_main,
    #         'metall_categories_similar': metall_categories_similar,
    #         'news_list': news_list,
    #         'advanteges_list': advanteges_list,
    #         'manufactures_list': manufactures_list,
    #         'awards_list': awards_list,
    #         'vacancy_list': vacancy_list,
    #         'sertificats_list': sertificats_list,
    #         'pricelist_list': pricelist_list,
    #         'text_blocks_menu': text_blocks_menu,
    #     }
    #     context.update(s_filter_options)
    #     context.update(applied_filters)
        
    #     # Définir le template à utiliser
    #     self.template_name = current_menu.typeMenu.template

    #     return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        menu_slug = kwargs.get('menu_slug')
        current_menu = get_object_or_404(MenuCatalog.objects.select_related('typeMenu', 'parent'), slug__iexact=menu_slug)
        
        # Redirection SEO si la casse de l'URL n'est pas correcte
        if 'filters_str' not in kwargs and 'page' not in kwargs and menu_slug != current_menu.slug:
            return HttpResponsePermanentRedirect(current_menu.get_absolute_url())

        # 1. Parser les filtres
        applied_filters = self._parse_filters_from_url(current_menu, **kwargs)
        
        # 2. Construire le queryset de base
        base_products_qs = self._get_base_product_queryset(current_menu)
        
        # 3. Générer les options de filtres disponibles (logique à facettes)
        qs_for_marka = self._apply_filters_to_queryset(base_products_qs, {**applied_filters, 'marka_lat': None})
        marka_filter_options = list(qs_for_marka.values('marka__name', 'marka__name_lat').order_by('marka__name').distinct())
        
        qs_for_gost = self._apply_filters_to_queryset(base_products_qs, {**applied_filters, 'gost_lat': None})
        gost_filter_options = list(qs_for_gost.values('gost__number', 'gost__number_lat').order_by('gost__number').distinct())
        
        s_filter_options = {}
        size_map_rev = {'size_a': 's1_lat', 'size_b': 's2_lat', 'size_c': 's3_lat', 'size_d': 's4_lat', 'size_e': 's5_lat', 'size_f': 's6_lat', 'size_l': 's7_lat'}
        for field, key in size_map_rev.items():
            temp_filters = applied_filters.copy()
            temp_filters[key] = None
            qs_for_size = self._apply_filters_to_queryset(base_products_qs, temp_filters)
            s_filter_options[f"{key.replace('_lat', '')}_filter"] = list(
                CatalogFilterValue.objects.filter(
                    filter_name__name_lat=field,
                    category=current_menu,
                    value__in=qs_for_size.values_list(field, flat=True).distinct()
                ).values('value', 'value_lat').distinct().order_by('value')
            )

        # 4. Filtrer les produits pour l'affichage final
        filtered_products_qs = self._apply_filters_to_queryset(base_products_qs, applied_filters)

        # --- CORRECTION N°1 : LIRE LA PAGE DEPUIS KWARGS ---
        # On lit le numéro de page depuis les arguments de l'URL (`kwargs`) en priorité.
        page_number = kwargs.get('page') or request.GET.get('page', 1)

        # 5. Pagination
        paginator = Paginator(filtered_products_qs.select_related('gost', 'marka'), SIZE_PAGE)
        page_obj = paginator.get_page(page_number)
        
        page_num = page_obj.number
        paginator_min = max(page_num - 5, 1)
        paginator_max = min(page_num + 5, paginator.num_pages)
        
        # --- CORRECTION N°2 : CONSTRUIRE L'URL DE BASE DES FILTRES ---
        # Cette variable sera utilisée par le template de pagination.
        base_filter_url_part = ""
        if filters_str := kwargs.get('filters_str'):
            base_filter_url_part = f"/f/{filters_str}"


        # 6. Récupérer les données annexes
        current_filial = get_current_filial(request.get_host())
        #dynamic_h1 = self._build_dynamic_h1(current_menu, applied_filters, current_filial)
        dynamic_h1 = self._build_dynamic_h1(current_menu, applied_filters, current_filial, page_number=page_obj.number)
        dop_text_block_url = TextBlockUrl.objects.filter(Q(url=request.path, filial=current_filial, isHidden=False) | Q(url=request.path, filial__isnull=True, isHidden=False)).order_by('-filial').first()
        current_menu_main = current_menu.get_parent_menu()
        metall_categories_similar = current_menu.get_metall_categories_similar()
        news_list = News.objects.filter(isHidden=False)
        advanteges_list = Advanteges.objects.filter(isHidden=False)
        manufactures_list = Manufactures.objects.filter(isHidden=False)
        awards_list = Awards.objects.filter(isHidden=False)
        vacancy_list = Vacancy.objects.filter(isHidden=False)
        sertificats_list = Sertificats.objects.filter(isHidden=False)
        pricelist_list = Pricelists.objects.filter(isHidden=False)
        text_blocks_menu = TextBlockMenu.objects.filter(position=current_menu)

        # 7. Construire le contexte
        context = {
            'current_menu': current_menu,
            'products': page_obj,
            'marka_filter_list': page_obj,
            'marka_filter': marka_filter_options,
            'gost_filter': gost_filter_options,
            'paginatorMin': paginator_min,
            'paginatorMax': paginator_max,
            'dynamic_h1': dynamic_h1,
            'base_filter_url_part': base_filter_url_part,

            # Données annexes
            'current_filial': current_filial,
            'dop_text_block_url': dop_text_block_url,
            'current_menu_main': current_menu_main,
            'metall_categories_similar': metall_categories_similar,
            'news_list': news_list,
            'advanteges_list': advanteges_list,
            'manufactures_list': manufactures_list,
            'awards_list': awards_list,
            'vacancy_list': vacancy_list,
            'sertificats_list': sertificats_list,
            'pricelist_list': pricelist_list,
            'text_blocks_menu': text_blocks_menu,
        }
        context.update(s_filter_options)
        context.update(applied_filters)
        
        # Définir le template à utiliser
        self.template_name = current_menu.typeMenu.template

        return render(request, self.template_name, context)


class ProductView(TemplateView):
    """
    Affiche la page de détail d'un produit.
    """
    template_name = "catalog/product.html"

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('product_slug')

        try:
            product = Product.objects.select_related(
                'catalog', 
                'catalog__parent', # Pré-charger le parent de la catégorie
                'catalog__typeMenu', # Pré-charger le type de menu
            ).get(slug__iexact=product_slug)
        except Product.DoesNotExist:
            raise Http404("Produit non trouvé")

        current_menu = product.catalog
        current_menu_main = current_menu.get_parent_menu() # Utilise la méthode du modèle

        sotrudniki_qs = SotrudnikiService.objects.filter(position=current_menu_main)
        sotrudnik = sotrudniki_qs.order_by('?').first() # Sélectionne un employé au hasard
        if not sotrudnik:
            sotrudnik = SotrudnikiService.objects.order_by('?').first()

        # 4. Logique pour changer de template
        if current_menu_main.name == "Производство":
            self.template_name = "catalog/proizvodstvo_one.html"
        elif current_menu_main.name == "Услуги":
            self.template_name = "info/usluga_one.html"

        # 5. Récupérer les produits similaires
        metall_categories_similar = Product.objects.filter(
            catalog=current_menu, isHidden=False
        ).exclude(pk=product.pk)[:4] # Exclure le produit actuel de sa propre liste de similaires

        # 6. Construire le contexte explicite
        context = {
            'product': product,
            'page_title': product.name,
            'meta_keywords': product.keywords,
            'meta_description': product.keywords_description,
            'current_menu': current_menu,
            'current_menu_main': current_menu_main,
            'sotrudnik': sotrudnik,
            'metall_categories_similar': metall_categories_similar,
        }

        response = render(request, self.template_name, context)

        if product.updated_at:
            response['Last-Modified'] = datetime2rfc(product.updated_at)
            last_modified_header = request.META.get('HTTP_IF_MODIFIED_SINCE')
            if last_modified_header:
                if _if_modified_since(datetime2rfc(product.updated_at), last_modified_header):
                    return HttpResponseNotModified()

        return response


def import_image(request, image_name, control_code, url_image, info=None, product_id=None):
    from admin_m.views import IND_STATE_ERROR

    if control_code != CONTROL_CODE:
        raise Http404()

    load_dir = os.path.join(settings.MEDIA_ROOT, "uploads/images/load/")
    path_image = os.path.join(load_dir, image_name)

    os.makedirs(load_dir, exist_ok=True)

    if not url_image.startswith(('http://', 'https://')):
        urls_to_try = [f'https://{url_image}', f'http://{url_image}']
    else:
        urls_to_try = [url_image]

    content = None
    for url in urls_to_try:
        try:
            # S'identifier comme un navigateur pour éviter les blocages 403 Forbidden
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=10) as response: # Ajout d'un timeout
                content = response.read()
                break # Arrêter à la première tentative réussie
        except (HTTPError, URLError) as e:
            # Si une erreur se produit, on passe à l'URL suivante (http si https a échoué)
            print(f"Échec du téléchargement de {url}: {e}")
            continue

    # Si le téléchargement a échoué pour toutes les tentatives
    if content is None:
        if info:
            error_msg = f"ОШИБКА 404 (или другая ошибка сети) при загрузке изображения продукта c id={int(product_id)} (URL: {url_image})\n"
            info.info += error_msg
            info.state_id = IND_STATE_ERROR
            info.save()
        return HttpResponseRedirect("/") # Rediriger même en cas d'erreur

    try:
        with open(path_image, 'wb') as out_file:
            out_file.write(content)
    except IOError as e:
        if info:
            info.info += f"ОШИБКА записи файла на disque для продукта id={int(product_id)}: {e}\n"
            info.state_id = IND_STATE_ERROR
            info.save()
        return HttpResponseRedirect("/")

    # Essayer d'ouvrir et de convertir l'image avec PIL
    try:
        with Image.open(path_image) as img:
            # Convertir en RGB pour standardiser (enlève la transparence, etc.) et sauvegarder
            img.convert('RGB').save(path_image, 'JPEG', quality=85)
    except IOError as e: # PIL lève IOError pour les fichiers corrompus/invalides
        if info:
            error_msg = f"ОШИБКА: Le fichier téléchargé для продукта id={int(product_id)} n'est pas une image valide (URL: {url_image}). Erreur PIL: {e}\n"
            info.info += error_msg
            info.state_id = IND_STATE_ERROR
            info.save()
        # On peut supprimer le fichier invalide pour ne pas polluer le disque
        os.remove(path_image)

    return HttpResponseRedirect("/")


def set_slug(request, id_product, control_code):
    if not control_code == CONTROL_CODE:
        raise Http404()
    try:
        product = Product.objects.get(id=int(id_product))
        product.set_slug()
        product.save()
    except:
        raise Http404()
    return HttpResponseRedirect("/")


def set_param_category(request, id_category, control_code):
    if not control_code == CONTROL_CODE:
        raise Http404()
    try:
        categoryMetall = MenuCatalog.objects.get(id=int(id_category))

        from catalog_filter.models import CatalogFilterValue
        from catalog_filter.models import CatalogFilterName

        CatalogFilterValue.objects.filter(category=categoryMetall.id).delete()

        current_list = Product.objects.filter(catalog=categoryMetall.id, isHidden=False)
        current_list |= Product.objects.filter(catalogOne=categoryMetall.id, isHidden=False)
        current_list |= Product.objects.filter(catalogTwo=categoryMetall.id, isHidden=False)
        current_list |= Product.objects.filter(catalogThree=categoryMetall.id, isHidden=False)

        if not categoryMetall.isHideMarka:
            marka_filter = list(map(itemgetter(0),groupby(current_list.values('marka__name','marka__name_lat').order_by('marka__name'))))
            for item in marka_filter:
                if item['marka__name']:
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="marka")[0]
                    new_item.value = item['marka__name']
                    new_item.value_lat = item['marka__name_lat']
                    new_item.is_hidden = False
                    new_item.save()

        if not categoryMetall.isHideGOST:
            gost_filter = list(map(itemgetter(0),groupby(current_list.values('gost__number','gost__number_lat').order_by('gost__number'))))
            for item in gost_filter:
                if item['gost__number']:
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="gost")[0]
                    new_item.value = item['gost__number']
                    new_item.value_lat = item['gost__number_lat']
                    new_item.is_hidden = False
                    new_item.save()

        if categoryMetall.labelSizeA:
            s1_filter = list(map(itemgetter(0),groupby(current_list.values('size_a').order_by('size_a'))))
            for item in s1_filter:
                if item['size_a'] and item['size_a'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_a")[0]
                    new_item.value = item['size_a']
                    new_item.value_lat = translit(item['size_a'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()

        if categoryMetall.labelSizeB:
            s2_filter = list(map(itemgetter(0),groupby(current_list.values('size_b').order_by('size_b'))))
            for item in s2_filter:
                if item['size_b'] and item['size_b'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_b")[0]
                    new_item.value = item['size_b']
                    new_item.value_lat = translit(item['size_b'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()

        if categoryMetall.labelSizeC:
            s3_filter = list(map(itemgetter(0),groupby(current_list.values('size_c').order_by('size_c'))))
            for item in s3_filter:
                if item['size_c'] and item['size_c'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_c")[0]
                    new_item.value = item['size_c']
                    new_item.value_lat = translit(item['size_c'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()

        if categoryMetall.labelSizeD:
            s4_filter = list(map(itemgetter(0),groupby(current_list.values('size_d').order_by('size_d'))))
            for item in s4_filter:
                if item['size_d'] and item['size_d'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_d")[0]
                    new_item.value = item['size_d']
                    new_item.value_lat = translit(item['size_d'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()

        if categoryMetall.labelSizeE:
            s5_filter = list(map(itemgetter(0),groupby(current_list.values('size_e').order_by('size_e'))))
            for item in s5_filter:
                if item['size_e'] and item['size_e'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_e")[0]
                    new_item.value = item['size_e']
                    new_item.value_lat = translit(item['size_e'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()
        if categoryMetall.labelSizeF:
            s6_filter = list(map(itemgetter(0),groupby(current_list.values('size_f').order_by('size_f'))))
            for item in s6_filter:
                if item['size_f'] and item['size_f'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_f")[0]
                    new_item.value = item['size_f']
                    new_item.value_lat = translit(item['size_f'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()
        if categoryMetall.labelSizeL:
            s7_filter = list(map(itemgetter(0),groupby(current_list.values('size_l').order_by('size_l'))))
            for item in s7_filter:
                if item['size_l'] and item['size_l'] != "0":
                    new_item = CatalogFilterValue()
                    new_item.category = categoryMetall
                    new_item.filter_name = CatalogFilterName.objects.filter(name_lat="size_l")[0]
                    new_item.value = item['size_l']
                    new_item.value_lat = translit(item['size_l'], "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
                    new_item.is_hidden = False
                    new_item.save()

        categoryMetall.save()
    except:
        raise Http404()
    return HttpResponseRedirect("/")


def get_json_products(request):
    products = Product.active.all()
    json_products = serializers.serialize("json", products)
    return HttpResponse(json_products, content_type='application/javascript; charset=utf-8')







# def handler404(request, exception, template_name="catalog/page404.html"):
#     """ Vue personnalisée pour les erreurs 404 (Page non trouvée). """
    
#     products_featured = []
#     products_men = []
#     products_women = []
#     page_title = 'Главная'
#     startPage = 1
#     startPageCatalog = 2
#     page404 = True
    
#     sliders = Slider.objects.filter(isHidden=False)
#     specpredlozh_list = SpecPredlozhenie.objects.filter(isShowMain=True, isHidden=False)
#     portfolio_list = Portfolio.objects.filter(isShowMain=True, isHidden=False)
#     news_list = News.objects.filter(isMain=True, isHidden=False).order_by("-date")[:2]
#     partners_list = Partners.objects.filter(isMain=True, isHidden=False)
#     advanteges_list = Advanteges.objects.filter(isMain=True, isHidden=False)
    
#     current_menu = None
#     current_menu_catalog = None
#     text_blocks_menu = None
    
#     try:
#         current_menu = MenuCatalog.objects.get(id=startPage)
#         current_menu_catalog = MenuCatalog.objects.get(id=startPageCatalog)
#         text_blocks_menu = TextBlockMenu.objects.filter(position__name="Главная").first()
#     except MenuCatalog.DoesNotExist:
#         pass
#     except TextBlockMenu.DoesNotExist:
#         pass

#     context = {
#         'products_featured': products_featured,
#         'products_men': products_men,
#         'products_women': products_women,
#         'page_title': page_title,
#         'page404': page404,
#         'sliders': sliders,
#         'specpredlozh_list': specpredlozh_list,
#         'portfolio_list': portfolio_list,
#         'news_list': news_list,
#         'partners_list': partners_list,
#         'advanteges_list': advanteges_list,
#         'current_menu': current_menu,
#         'current_menu_catalog': current_menu_catalog,
#         'text_blocks_menu': text_blocks_menu,
#     }

#     response = render(request, template_name, context)
#     response.status_code = 404
#     return response


def handler404(request, exception, template_name="catalog/page404.html"):
    """
    Gestionnaire optimisé pour les erreurs 404 (Page Non Trouvée).
    Délègue la plupart du travail au context processor global_views.
    """
    
    # 1. Récupérer des produits pertinents à suggérer à l'utilisateur.
    # Au lieu de charger des listes aléatoires, on suggère les produits les plus populaires.
    
    try:
        # On compte le nombre de fois que chaque produit apparaît dans les commandes
        # et on prend les 4 plus populaires. C'est une suggestion utile.
        popular_products = Product.objects.filter(
            isHidden=False, 
            orderitem__isnull=False # S'assurer qu'ils sont dans au moins une commande
        ).annotate(
            order_count=Count('orderitem') # Compter les occurrences
        ).order_by(
            '-order_count' # Trier par popularité décroissante
        ).select_related(
            'catalog' # Pré-charger la catégorie pour éviter les requêtes N+1 dans le template
        )[:4]

    except Exception:
        # En cas d'erreur (si le modèle OrderItem n'est pas encore importé, etc.),
        # on se rabat sur une simple liste de produits récents.
        popular_products = Product.objects.filter(isHidden=False).select_related('catalog').order_by('-updated_at')[:4]

    # 2. Construire un contexte MINIMALISTE.
    # Toutes les variables globales (menus, filiales, contacts...) seront ajoutées
    # automatiquement par votre context processor `global_views`.
    # Nous n'ajoutons que ce qui est spécifique à CETTE page.
    context = {
        'page_title': 'Страница не найдена (404)',
        'metall_categories_similar': popular_products, # Le template 'page404.html' s'attend à cette variable
        'page404': True, # Pour que le template sache qu'il s'agit d'une page 404
    }

    # 3. Rendre la réponse avec le statut HTTP correct.
    # Le 'status=404' est la manière moderne de le faire.
    return render(request, template_name, context, status=404)


def handler500(request, template_name="catalog/page500.html"):
    """ Vue personnalisée pour les erreurs 500 (Erreur serveur). """
    
    context = {
        'page_title': 'Ошибка сервера',
    }
    
    response = render(request, template_name, context)
    response.status_code = 500
    return response

