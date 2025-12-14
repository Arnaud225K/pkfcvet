# from django import template
# from search.forms import SearchForm
# import urllib

# register = template.Library()


# @register.inclusion_tag("tags/search_box.html")
# def search_box(request):
#     q = request.GET.get('q','')
#     form = SearchForm({'q': q })
#     return {'form': form }


# @register.inclusion_tag('tags/pagination_links.html')
# def pagination_links(request, paginator):
#     raw_params = request.GET.copy()
#     page = raw_params.get('page',1)
#     p = paginator.page(page)
#     try:
#         del raw_params['page']
#     except KeyError:
#         pass
#     # params = urllib.urlencode(raw_params)
#     try:
#         if raw_params['s_gost']:
#             params = "s_gost="+raw_params['s_gost']
#     except:
#         try:
#             if raw_params['s_marka']:
#                 params = "s_marka="+raw_params['s_marka']
#         except:
#             params = "s="+raw_params['s']
#     return {'request': request,
#             'paginator': paginator,
#             'p': p,
#             'params': params }


# search/templatetags/search_tags.py

from django import template
from search.forms import SearchForm
from urllib.parse import urlencode # <-- CHANGEMENT ICI

register = template.Library()


@register.inclusion_tag("tags/search_box.html")
def search_box(request):
    q = request.GET.get('q', '') # Le paramètre de recherche est 's', pas 'q' dans votre vue
    q = request.GET.get('s', '')
    form = SearchForm({'q': q})
    return {'form': form}


@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator, page_obj): # <-- CHANGEMENT ICI
    """
    Génère les liens de pagination.
    Reçoit l'objet Paginator et l'objet Page directement depuis la vue.
    """
    # 1. Récupérer tous les paramètres GET de la requête actuelle
    raw_params = request.GET.copy()
    
    # 2. Supprimer le paramètre 'page' s'il existe, pour éviter les doublons
    if 'page' in raw_params:
        del raw_params['page']
        
    # 3. Encoder le reste des paramètres dans une chaîne URL-safe
    # Ex: {'s': 'test'} -> 's=test'
    params = urlencode(raw_params)
    
    # 4. Retourner le contexte pour le template de pagination
    return {
        'request': request,
        'paginator': paginator,
        'page_obj': page_obj, # On passe l'objet page
        'params': params,     # La chaîne de paramètres pour les liens
    }