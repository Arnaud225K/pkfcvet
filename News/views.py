# # -*- coding: utf-8 -*-
# from News.models import News
# from django.shortcuts import render, get_object_or_404
# from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core import urlresolvers
# from django.views.decorators.cache import cache_page
# from django.views.decorators.csrf import requires_csrf_token

# from menu.models import MenuCatalog, Product
# import pkfcvet.settings as settings

# SLUG_PAGE_NEWS = "news"
# SLUG_PAGE_ARTICLES = "articles"


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def news_all(request, page=0, template_name="sys/news.html"):
#     try:
#         page = int(page)
#     except:
#         raise Http404()
#     SIZE_PAGE_NEWS = 4
#     SIZE_PAGE_LAST_NEWS = 4
#     URL_PAGE_NEWS = "/news/"
#     current_menu = get_object_or_404(MenuCatalog, slug=SLUG_PAGE_NEWS)
#     news_list = News.objects.filter(articles_flag=False,isHidden=False)
#     news_list_last = news_list[:SIZE_PAGE_LAST_NEWS]

#     # currentMenu = Menu.objects.get(id=ID_NEWS_PAGE)
#     # oneNews = News.objects.get(id=offset)
#     paginatorMin = 1
#     paginatorMax = 5
#     paginator = Paginator(news_list, SIZE_PAGE_NEWS)

#     if page == 1 or page > paginator.num_pages:
#         return HttpResponseRedirect(URL_PAGE_NEWS)
#     if page == 0:
#         page = 1

#     try:
#         news_list = paginator.page(page)

#         if int(page) < 5:
#             paginatorMin = 1
#             paginatorMax = 5
#         else:
#             paginatorMin = max(int(page)-2,1)
#             paginatorMax = min(int(page)+2,paginator.num_pages)

#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         news_list = paginator.page(1)

#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         news_list = paginator.page(paginator.num_pages)

#     response = render(request, template_name, locals())
#     return response



# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def news_one(request, news_slug=None, template_name="sys/news.html"):
#     news_one = get_object_or_404(News, name_lat=news_slug, articles_flag=False)
#     #На случай, если идет окончание оформления заявки
#     order_number = request.session.get('order_number','')
#     if order_number:
#         receipt_url = urlresolvers.reverse('checkout_receipt')
#         return HttpResponseRedirect(receipt_url)

#     current_menu = get_object_or_404(MenuCatalog, slug=SLUG_PAGE_NEWS)
#     SIZE_PAGE_LAST_NEWS = 5 #на случай если выбранная новость - одна из последних
#     URL_PAGE_NEWS = "/news/"
#     news_list = News.objects.filter(articles_flag=False, isHidden=False)
#     news_list_last = news_list[:SIZE_PAGE_LAST_NEWS]
#     if not (news_one in news_list_last):#на случай если выбранная новость - одна из последних
#         SIZE_PAGE_LAST_NEWS = 4
#         news_list_last = news_list[:SIZE_PAGE_LAST_NEWS]

#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    



# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def articles_all(request, page=0, template_name="sys/articles.html"):
#     try:
#         page = int(page)
#     except:
#         raise Http404()
#     SIZE_PAGE_ARTICLES = 4
#     SIZE_PAGE_LAST_ARTICLES = 4
#     URL_PAGE_ARTICLES = "/articles/"
#     current_menu = get_object_or_404(MenuCatalog, slug=SLUG_PAGE_ARTICLES)
#     art_list = News.objects.filter(articles_flag=True, isHidden=False)
#     art_list_last = art_list[:SIZE_PAGE_LAST_ARTICLES]


#     # currentMenu = Menu.objects.get(id=ID_NEWS_PAGE)
#     # oneNews = News.objects.get(id=offset)
#     paginatorMin = 1
#     paginatorMax = 5
#     paginator = Paginator(art_list, SIZE_PAGE_ARTICLES)

#     if page == 1 or page > paginator.num_pages:
#         return HttpResponseRedirect(URL_PAGE_ARTICLES)
#     if page == 0:
#         page = 1

#     try:
#         art_list = paginator.page(page)

#         if int(page) < 5:
#             paginatorMin = 1
#             paginatorMax = 5
#         else:
#             paginatorMin = max(int(page)-2,1)
#             paginatorMax = min(int(page)+2,paginator.num_pages)

#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         art_list = paginator.page(1)

#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         art_list = paginator.page(paginator.num_pages)

#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def articles_one(request, articles_slug=None, template_name="sys/articles.html"):
#     art_one = get_object_or_404(News, name_lat=articles_slug)

#     link_1 = None
#     link_2 = None
#     link_3 = None
#     link_4 = None
#     try:
#         link_1 = MenuCatalog.objects.get(slug=art_one.nameLatCat_1)
#     except:
#         try:
#             link_1 = Product.objects.get(slug=art_one.nameLatCat_1)
#         except:
#             pass
#     try:
#         link_2 = MenuCatalog.objects.get(slug=art_one.nameLatCat_2)
#     except:
#         try:
#             link_2 = Product.objects.get(slug=art_one.nameLatCat_2)
#         except:
#             pass
#     try:
#         link_3 = MenuCatalog.objects.get(slug=art_one.nameLatProd_1)
#     except:
#         try:
#             link_3 = Product.objects.get(slug=art_one.nameLatProd_1)
#         except:
#             pass
#     try:
#         link_4 = MenuCatalog.objects.get(slug=art_one.nameLatProd_2)
#     except:
#         try:
#             link_4 = Product.objects.get(slug=art_one.nameLatProd_2)
#         except:
#             pass

#     #На случай, если идет окончание оформления заявки
#     order_number = request.session.get('order_number','')
#     if order_number:
#         receipt_url = urlresolvers.reverse('checkout_receipt')
#         return HttpResponseRedirect(receipt_url)

#     current_menu = get_object_or_404(MenuCatalog, slug=SLUG_PAGE_ARTICLES)
#     SIZE_PAGE_LAST_ARTICLES = 4 #на случай если выбранная новость - одна из последних
#     URL_PAGE_ARTICLES = "/articles/"
#     art_list = News.objects.filter(articles_flag=True, isHidden=False)
#     art_list_last = art_list[:SIZE_PAGE_LAST_ARTICLES]
#     if not (art_one in art_list_last):#на случай если выбранная новость - одна из последних
#         SIZE_PAGE_LAST_ARTICLES = 3
#         art_list_last = art_list[:SIZE_PAGE_LAST_ARTICLES]

#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))



# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.urls import reverse
# from django.views.decorators.cache import cache_page

# from .models import News 
# from menu.models import MenuCatalog, Product
# import pkfcvet.settings as settings

# SLUG_PAGE_NEWS = "news"
# SLUG_PAGE_ARTICLES = "articles"


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def news_all(request, page=0, template_name="sys/news.html"):
#     try:
#         page = int(page)
#     except (ValueError, TypeError):
#         raise Http404()

#     SIZE_PAGE_NEWS = 4
#     SIZE_PAGE_LAST_NEWS = 4
#     URL_PAGE_NEWS = reverse('news_list')

#     current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_NEWS)
#     news_list_qs = News.objects.filter(articles_flag=False, isHidden=False)
#     news_list_last = news_list_qs[:SIZE_PAGE_LAST_NEWS]

#     paginator = Paginator(news_list_qs, SIZE_PAGE_NEWS)

#     if page == 1 or page > paginator.num_pages:
#         return redirect(URL_PAGE_NEWS)
#     if page == 0:
#         page = 1

#     try:
#         news_list_page = paginator.page(page)
#     except PageNotAnInteger:
#         news_list_page = paginator.page(1)
#     except EmptyPage:
#         news_list_page = paginator.page(paginator.num_pages)
    
#     paginatorMin = max(page - 2, 1)
#     paginatorMax = min(page + 2, paginator.num_pages)

#     context = {
#         'current_menu': current_menu,
#         'news_list': news_list_page,
#         'news_list_last': news_list_last,
#         'paginatorMin': paginatorMin,
#         'paginatorMax': paginatorMax,
#     }
#     return render(request, template_name, context)


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def news_one(request, news_slug=None, template_name="sys/news.html"):
#     news_one = get_object_or_404(News, name_lat__iexact=news_slug, articles_flag=False)

#     order_number = request.session.get('order_number', '')
#     if order_number:
#         receipt_url = reverse('checkout_receipt')
#         return redirect(receipt_url)

#     current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_NEWS)
#     SIZE_PAGE_LAST_NEWS = 4
#     news_list_qs = News.objects.filter(articles_flag=False, isHidden=False)
#     news_list_last = list(news_list_qs[:SIZE_PAGE_LAST_NEWS + 1])
    
#     if news_one in news_list_last:
#         news_list_last.remove(news_one)
    
#     news_list_last = news_list_last[:SIZE_PAGE_LAST_NEWS]

#     context = {
#         'news_one': news_one,
#         'current_menu': current_menu,
#         'news_list_last': news_list_last,
#     }
#     return render(request, template_name, context)


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def articles_all(request, page=0, template_name="sys/articles.html"):
#     try:
#         page = int(page)
#     except (ValueError, TypeError):
#         raise Http404()
    
#     SIZE_PAGE_ARTICLES = 4
#     URL_PAGE_ARTICLES = reverse('news:news_list')

#     current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_ARTICLES)
#     art_list_qs = News.objects.filter(articles_flag=True, isHidden=False)
#     art_list_last = art_list_qs[:SIZE_PAGE_ARTICLES]

#     paginator = Paginator(art_list_qs, SIZE_PAGE_ARTICLES)

#     if page == 1 or page > paginator.num_pages:
#         return redirect(URL_PAGE_ARTICLES)
#     if page == 0:
#         page = 1

#     try:
#         art_list_page = paginator.page(page)
#     except PageNotAnInteger:
#         art_list_page = paginator.page(1)
#     except EmptyPage:
#         art_list_page = paginator.page(paginator.num_pages)
    
#     paginatorMin = max(page - 2, 1)
#     paginatorMax = min(page + 2, paginator.num_pages)

#     context = {
#         'current_menu': current_menu,
#         'art_list': art_list_page,
#         'art_list_last': art_list_last,
#         'paginatorMin': paginatorMin,
#         'paginatorMax': paginatorMax,
#     }
#     return render(request, template_name, context)


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def articles_one(request, articles_slug=None, template_name="sys/articles.html"):
#     art_one = get_object_or_404(News, name_lat__iexact=articles_slug)

#     links = []
#     slugs_to_check = [
#         art_one.nameLatCat_1,
#         art_one.nameLatCat_2,
#         art_one.nameLatProd_1,
#         art_one.nameLatProd_2,
#     ]
#     for slug in slugs_to_check:
#         if not slug:
#             continue
#         try:
#             links.append(MenuCatalog.objects.get(slug__iexact=slug))
#         except MenuCatalog.DoesNotExist:
#             try:
#                 links.append(Product.objects.get(slug__iexact=slug))
#             except Product.DoesNotExist:
#                 pass
    
#     order_number = request.session.get('order_number', '')
#     if order_number:
#         receipt_url = reverse('checkout_receipt')
#         return redirect(receipt_url)

#     current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_ARTICLES)
#     SIZE_PAGE_LAST_ARTICLES = 4
#     art_list_qs = News.objects.filter(articles_flag=True, isHidden=False)
#     art_list_last = list(art_list_qs[:SIZE_PAGE_LAST_ARTICLES + 1])
    
#     if art_one in art_list_last:
#         art_list_last.remove(art_one)
    
#     art_list_last = art_list_last[:SIZE_PAGE_LAST_ARTICLES]

#     context = {
#         'art_one': art_one,
#         'links': links,
#         'current_menu': current_menu,
#         'art_list_last': art_list_last,
#     }
#     return render(request, template_name, context)



# News/views.py

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.http import Http404, HttpResponse, HttpResponseRedirect


# Importer les modèles nécessaires
from menu.models import MenuCatalog, Product
from .models import News


# Constantes pour éviter les "chaînes magiques"
SLUG_PAGE_NEWS = "news"
SLUG_PAGE_ARTICLES = "articles"


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def news_all(request, page=1): # page=1 par défaut est plus sûr
#     # La conversion en int est gérée par le système d'URL
    
#     SIZE_PAGE_NEWS = 4
#     SIZE_PAGE_LAST_NEWS = 4
    
#     # <-- CORRECTION ICI : Nom de l'URL
#     URL_PAGE_NEWS = reverse('news:news_list')

#     current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_NEWS)
    
#     # On utilise select_related pour pré-charger le type de news si nécessaire
#     news_list_qs = News.objects.filter(articles_flag=False, isHidden=False).select_related('type')
#     news_list_last = news_list_qs[:SIZE_PAGE_LAST_NEWS]

#     paginator = Paginator(news_list_qs, SIZE_PAGE_NEWS)
    
#     # Redirection si la page 1 est demandée avec un numéro de page dans l'URL
#     if page == 1:
#         return redirect(URL_PAGE_NEWS, permanent=True)

#     news_list_page = paginator.get_page(page)
    
#     paginatorMin = max(news_list_page.number - 2, 1)
#     paginatorMax = min(news_list_page.number + 2, paginator.num_pages)

#     context = {
#         'current_menu': current_menu,
#         'news_list': news_list_page,
#         'news_list_last': news_list_last,
#         'paginatorMin': paginatorMin,
#         'paginatorMax': paginatorMax,
#     }
#     return render(request, "sys/news.html", context)

@cache_page(settings.CACHE_TIME_BASE_VIEW)
def news_all(request, page=None):
    """
    Affiche la liste paginée des news.
    Corrigé pour éviter les boucles de redirection.
    """
    # Si 'page' est fourni dans l'URL, on le convertit en entier. Sinon, c'est la page 1.
    page_num = 1
    if page:
        try:
            page_num = int(page)
        except (ValueError, TypeError):
            raise Http404("Le numéro de page doit être un entier.")

        # Si quelqu'un accède à la page 1 via l'URL paginée (ex: /news/1/),
        # on le redirige vers l'URL canonique (/news/) pour éviter le contenu dupliqué.
        if page_num == 1:
            return redirect('news:news_list', permanent=True)

    SIZE_PAGE_NEWS = 4
    SIZE_PAGE_LAST_NEWS = 4

    current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_NEWS)
    
    news_list_qs = News.objects.filter(articles_flag=False, isHidden=False)
    news_list_last = news_list_qs[:SIZE_PAGE_LAST_NEWS]

    paginator = Paginator(news_list_qs, SIZE_PAGE_NEWS)
    
    # get_page gère les pages invalides (lettres, trop grandes, etc.)
    news_list_page = paginator.get_page(page_num)
    
    # Logique pour la plage du paginateur
    paginatorMin = max(news_list_page.number - 2, 1)
    paginatorMax = min(news_list_page.number + 2, paginator.num_pages)

    context = {
        'current_menu': current_menu,
        'news_list': news_list_page,
        'news_list_last': news_list_last,
        'paginatorMin': paginatorMin,
        'paginatorMax': paginatorMax,
    }
    return render(request, "sys/news.html", context)


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def news_one(request, news_slug=None):
    # La recherche insensible à la casse est déjà correcte ici
    news_one = get_object_or_404(News, name_lat__iexact=news_slug, articles_flag=False)

    # La vérification de la session est bonne, on la garde
    order_number = request.session.get('order_number')
    if order_number:
        return redirect('checkout:checkout_receipt')

    current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_NEWS)
    
    SIZE_PAGE_LAST_NEWS = 4
    # On exclut la news actuelle de la liste des dernières news
    news_list_last = News.objects.filter(
        articles_flag=False, isHidden=False
    ).exclude(pk=news_one.pk)[:SIZE_PAGE_LAST_NEWS]

    context = {
        'news_one': news_one,
        'current_menu': current_menu,
        'news_list_last': news_list_last,
    }
    return render(request, "sys/news_one.html", context) # Utiliser un template dédié est mieux


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def articles_all(request, page=1):
#     SIZE_PAGE_ARTICLES = 4
    
#     # <-- CORRECTION ICI : Nom de l'URL
#     # URL_PAGE_ARTICLES = reverse('news:articles_list')
#     URL_PAGE_ARTICLES = reverse('articles:articles_list')


#     current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_ARTICLES)
    
#     art_list_qs = News.objects.filter(articles_flag=True, isHidden=False)
#     art_list_last = art_list_qs[:SIZE_PAGE_ARTICLES]

#     paginator = Paginator(art_list_qs, SIZE_PAGE_ARTICLES)

#     if page == 1:
#         return redirect(URL_PAGE_ARTICLES, permanent=True)

#     art_list_page = paginator.get_page(page)
    
#     paginatorMin = max(art_list_page.number - 2, 1)
#     paginatorMax = min(art_list_page.number + 2, paginator.num_pages)

#     context = {
#         'current_menu': current_menu,
#         'art_list': art_list_page,
#         'art_list_last': art_list_last,
#         'paginatorMin': paginatorMin,
#         'paginatorMax': paginatorMax,
#     }
#     return render(request, "sys/articles.html", context)

@cache_page(settings.CACHE_TIME_BASE_VIEW)
def articles_all(request, page=None):
    """
    Affiche la liste paginée des articles.
    Corrigé pour éviter les boucles de redirection.
    """
    # Si 'page' est fourni dans l'URL, on le convertit en entier. Sinon, c'est la page 1.
    page_num = 1
    if page:
        try:
            page_num = int(page)
        except (ValueError, TypeError):
            raise Http404("Le numéro de page doit être un entier.")
            
        # Si quelqu'un accède à la page 1 via l'URL paginée (ex: /articles/1/),
        # on le redirige vers l'URL canonique (/articles/) pour éviter le contenu dupliqué.
        if page_num == 1:
            return redirect('articles:articles_list', permanent=True)

    SIZE_PAGE_ARTICLES = 4
    
    # La correction du NoReverseMatch que vous aviez faite est correcte
    URL_PAGE_ARTICLES = reverse('articles:articles_list')

    current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_ARTICLES)
    
    art_list_qs = News.objects.filter(articles_flag=True, isHidden=False)
    art_list_last = art_list_qs[:SIZE_PAGE_ARTICLES]

    paginator = Paginator(art_list_qs, SIZE_PAGE_ARTICLES)
    
    art_list_page = paginator.get_page(page_num)
    
    paginatorMin = max(art_list_page.number - 2, 1)
    paginatorMax = min(art_list_page.number + 2, paginator.num_pages)

    context = {
        'current_menu': current_menu,
        'art_list': art_list_page,
        'art_list_last': art_list_last,
        'paginatorMin': paginatorMin,
        'paginatorMax': paginatorMax,
        'URL_PAGE_ARTICLES': URL_PAGE_ARTICLES, # On le passe au contexte si le template en a besoin
    }
    return render(request, "sys/articles.html", context)


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def articles_one(request, articles_slug=None):
    art_one = get_object_or_404(News, name_lat__iexact=articles_slug, articles_flag=True)

    # Logique pour trouver les liens (optimisée)
    links = []
    slugs_to_check = filter(None, [
        art_one.nameLatCat_1, art_one.nameLatCat_2,
        art_one.nameLatProd_1, art_one.nameLatProd_2,
    ])
    
    if slugs_to_check:
        # On fait une seule requête pour les catégories et une seule pour les produits
        menu_links = list(MenuCatalog.objects.filter(slug__in=slugs_to_check))
        product_links = list(Product.objects.filter(slug__in=slugs_to_check))
        links = menu_links + product_links
    
    order_number = request.session.get('order_number')
    if order_number:
        return redirect('checkout:checkout_receipt')

    current_menu = get_object_or_404(MenuCatalog, slug__iexact=SLUG_PAGE_ARTICLES)
    
    SIZE_PAGE_LAST_ARTICLES = 4
    art_list_last = News.objects.filter(
        articles_flag=True, isHidden=False
    ).exclude(pk=art_one.pk)[:SIZE_PAGE_LAST_ARTICLES]

    context = {
        'art_one': art_one,
        'links': links,
        'current_menu': current_menu,
        'art_list_last': art_list_last,
    }
    return render(request, "sys/articles_one.html", context) # Utiliser un template dédié