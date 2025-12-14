from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from . import searchpy as search
from django.conf import settings

def results(request, template_name="search/results.html"):
    flag_gost = False
    flag_marka = False
    
    q = request.GET.get('s', '')
    
    results = []
    matching = [] 
    paginator = None 
    q_change = q

    if q:
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
        
        if flag_gost:
            matching = search.gosts(q).get('products', []) 
        elif flag_marka:
            matching = search.markas(q).get('products', []) 
        else:
            res_search = search.products(q)
            matching = res_search.get('products', []) 
            q_change = res_search.get('search_text', q)

        if matching:
            paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)
            # Utiliser get_page est plus sûr et gère les erreurs automatiquement
            page_obj = paginator.get_page(page) 
            results = page_obj.object_list
        else:
            page_obj = None

        if page == 1:
            search.store(request, q, q_change)
    else:
        page_obj = None

    page_title = 'Результаты поиска: ' + q

    context = {
        'q': q,
        'q_change': q_change,
        'results': results,
        'page_title': page_title,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template_name, context)