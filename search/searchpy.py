# # -*- coding: utf-8 -*-
# from search.models import SearchTerm, SearchChange, SearchRemove
# from menu.models import Product
# from GOST.models import GOST
# from Marochnik.models import MarkaMetall
# from django.db.models import Q
# from django.db.models import Count
# from Filials.models import Filials
# from menu.views_form import get_current_filial

# from stats import statspy as stats

# STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
#                'of', 'on', 'or', 'that', 'the', 'to', 'with']

# SEARCH_MAX_PRODUCTS = 300


# # store the search text in the database
# def store(request, q, q_change):
#     current_host = request.get_host()
#     current_filial = None
#     current_filial_city = None
#     #Формирование текстовых блоков для выбранного региона
#     # filials = Filials.objects.filter(isHidden=False)
#     # current_filial = None
#     # if filials:
#     #     current_filial = filials[0]
#     # filials_all = Filials.objects.all()
#     # for item in filials_all:
#     #     if item.subdomain_name and item.subdomain_name in current_host:
#     #         current_filial = item
#     host = request.get_host()
#     current_filial = get_current_filial(host)

#     # if search term is at least three chars long, store in db
#     page_path = request.GET.get('page_path', '')
#     if len(q) > 2:
#         term = SearchTerm()
#         term.q = q
#         term.q_change = q_change
#         term.path_site = page_path
#         term.filial_name = current_filial.name
#         term.subdomain_name = current_filial.subdomain_name
#         term.ip_address = request.META.get('REMOTE_ADDR')
#         term.tracking_id = stats.tracking_id(request)
#         term.user = None
#         if request.user.is_authenticated:
#             term.user = request.user
#         term.save()

# def is_float(str):
#     try:
#         float(str)
#         return True
#     except ValueError:
#         return False


# def products(search_text):
#     words = _prepare_words(search_text)
#     products = Product.objects.filter(isHidden=False)

#     results = {}
#     results['products'] = []
#     search_text_change = ""
#     for item in words:
#         search_text_change += (item.replace(',', '.') + " ")
#     results['search_text'] = search_text_change
#     results_id = []

#     i = 0

#     full_search_str = u""

#     index_size = 1  # Переменная для определения какой по счету ищется размер
#     for word in words:
#         word = word.replace(',', '.')

#         try:
#             cur_word_sinonim = SearchChange.objects.get(source=word)
#             words_sinonim = SearchChange.objects.filter(result=cur_word_sinonim.result)
#         except:
#             words_sinonim = []

#         if words_sinonim:
#             full_search_str += u"+("
#             for tmp_item in words_sinonim:
#                 item = tmp_item.source
#                 full_search_str += u"{} ".format(item)
#             full_search_str += u") "
#         else:
#             full_search_str += u"+{} ".format(word)
#         i = i + 1
#     # products = products.filter(name_main__search=full_search_str).only('slug', 'name_main')
        
#     products = products.filter(name_main__icontains=full_search_str).only('slug', 'name_main')

#     results['products'] = products

#     return results


# # get products matching the search text
# def gosts(search_text):
#     words = _prepare_words(search_text)
#     products = GOST.objects.all()
#     results = {}
#     results['products'] = []
#     # iterate through keywords
#     i = 0
#     for word in words:
#         products = products.filter(Q(name__icontains=unicode(word)) |
#                                    Q(number__icontains=unicode(word))|
#                                    Q(comment__icontains=unicode(word)))
#         #results['products'] += products
#         if i==0:
#            results['products'] =  products
#         else:
#             tmp_result = []
#             for item in products:
#                 if item in results['products']:
#                     tmp_result.append(item)
#             results['products'] = tmp_result
#         i = i + 1
#     return results


# # get products matching the search text
# def markas(search_text):
#     words = _prepare_words(search_text)
#     products = MarkaMetall.objects.all()
#     results = {}
#     results['products'] = []
#     # iterate through keywords
#     i = 0
#     for word in words:
#         products = products.filter(Q(name__icontains=unicode(word)) |
#                                    Q(comment__icontains=unicode(word)))
#         #results['products'] += products
#         if i==0:
#            results['products'] =  products
#         else:
#             tmp_result = []
#             for item in products:
#                 if item in results['products']:
#                     tmp_result.append(item)
#             results['products'] = tmp_result
#         i = i + 1
#     return results


# # strip out common words, limit to 5 words
# def _prepare_words(search_text):
#     # search_text = "графитовые стержни ду купить"
#     words = search_text.split()

#     for common in STRIP_WORDS:
#         if common in words:
#             words.remove(common)

#     words_blacklist = SearchRemove.objects.all()
#     for item in words_blacklist:
#         if item.str_remove in words:
#             words.remove(item.str_remove)

#     return words[0:15]



# search/searchpy.py

from .models import SearchTerm, SearchChange, SearchRemove
from menu.models import Product
from GOST.models import GOST
from Marochnik.models import MarkaMetall
from Filials.models import Filials
from menu.views_form import get_current_filial
from stats import statspy as stats

from django.db.models import Q

# Pas besoin d'importer Count ici

STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
               'of', 'on', 'or', 'that', 'the', 'to', 'with']

SEARCH_MAX_PRODUCTS = 300


def store(request, q, q_change):
    """Enregistre le terme de recherche dans la base de données."""
    host = request.get_host()
    current_filial = get_current_filial(host)

    if len(q) > 2 and current_filial:
        term = SearchTerm()
        term.q = q
        term.q_change = q_change
        term.path_site = request.GET.get('page_path', '')
        term.filial_name = current_filial.name
        term.subdomain_name = current_filial.subdomain_name
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        
        # <-- CHANGEMENT ICI : is_authenticated est un attribut
        if request.user.is_authenticated:
            term.user = request.user
        term.save()

def is_float(value):
    """Vérifie si une chaîne peut être convertie en float."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def products(search_text):
    """Recherche des produits correspondant au texte."""
    words = _prepare_words(search_text)
    
    results = {}
    results['products'] = []
    
    # Remplacer les virgules par des points et joindre les mots
    search_text_change = " ".join(word.replace(',', '.') for word in words)
    results['search_text'] = search_text_change
    
    # La logique de full_search_str était complexe et spécifique à MySQL full-text.
    # Pour une recherche __icontains simple, on utilise directement search_text_change.
    # Si on a besoin de chercher chaque mot individuellement, on peut construire une Q.
    
    # Recherche simple : le texte entier doit être trouvé
    # products_qs = Product.objects.filter(isHidden=False, name_main__icontains=search_text_change)
    
    # Recherche plus flexible : TOUS les mots doivent être présents
    products_qs = Product.objects.filter(isHidden=False)
    for word in words:
        products_qs = products_qs.filter(name_main__icontains=word)
    
    results['products'] = products_qs.only('slug', 'name_main')[:SEARCH_MAX_PRODUCTS]

    return results


def gosts(search_text):
    """Recherche des GOSTs. Version optimisée."""
    words = _prepare_words(search_text)
    if not words:
        return {'products': GOST.objects.none()}

    # Construire une requête qui cherche tous les mots dans n'importe quel champ
    query = Q()
    for word in words:
        # <-- CHANGEMENT ICI : unicode() -> str()
        query &= (Q(name__icontains=str(word)) |
                  Q(number__icontains=str(word)) |
                  Q(comment__icontains=str(word)))
        
    results_qs = GOST.objects.filter(query)
    
    return {'products': results_qs}


def markas(search_text):
    """Recherche des MarkaMetall. Version optimisée."""
    words = _prepare_words(search_text)
    if not words:
        return {'products': MarkaMetall.objects.none()}

    query = Q()
    for word in words:
        # <-- CHANGEMENT ICI : unicode() -> str()
        query &= (Q(name__icontains=str(word)) |
                  Q(comment__icontains=str(word)))

    results_qs = MarkaMetall.objects.filter(query)
    
    return {'products': results_qs}


def _prepare_words(search_text):
    """Nettoie et prépare les mots pour la recherche."""
    if not search_text:
        return []
    
    words = search_text.split()
    
    # Filtrer les mots courants
    words = [w for w in words if w.lower() not in STRIP_WORDS]

    # Filtrer les mots de la blacklist
    blacklist = SearchRemove.objects.values_list('str_remove', flat=True)
    words = [w for w in words if w not in blacklist]

    return words[:15]