# -*- coding: utf-8 -*-
# from django.shortcuts import render_to_response, get_object_or_404
# from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.views.decorators.cache import cache_page
# from django.views.decorators.csrf import requires_csrf_token
# from django.template import RequestContext
# from menu.models import MenuCatalog, Product
# from GOST.models import GOST, GOSTGroup, GOSTHead
# from cart.forms import ProductAddToCartForm
# from cart import cartpy
# import pkfcvet.settings as settings



# def GostHeadV(request,menuId ,gostHeadId):
#     try:
#         menuId = int(menuId)
#     except ValueError:
#         raise Http404()
#     try:
#         gostHeadId = int(gostHeadId)
#     except ValueError:
#         raise Http404()

#     currentMenu = MenuCatalog.objects.get(id=menuId)
#     gostHead = GOSTHead.objects.get(id=gostHeadId)
#     gostGroups = GOSTGroup.objects.filter(position=gostHeadId)



#     return render_to_response('index.html', {
#                               'currentMenu' : currentMenu,
#                               'oneGostHead' : gostHead,
#                               'gostGroups' : gostGroups,
#                               },
#                               context_instance=RequestContext(request), )

# def GostGroupV(request,menuId,gostHeadId ,gostGroupId):
#     try:
#         menuId = int(menuId)
#     except ValueError:
#         raise Http404()
#     try:
#         gostHeadId = int(gostHeadId)
#     except ValueError:
#         raise Http404()
#     try:
#         gostGroupId = int(gostGroupId)
#     except ValueError:
#         raise Http404()

#     currentMenu = MenuCatalog.objects.get(id=menuId)
#     gostHead = GOSTHead.objects.get(id=gostHeadId)
#     gostGroup = GOSTGroup.objects.get(id=gostGroupId)
#     gosts = GOST.objects.filter(position=gostGroupId)



#     return render_to_response('index.html', {
#                               'currentMenu' : currentMenu,
#                               'oneGostHead' : gostHead,
#                               'oneGostGroup' : gostGroup,
#                               'gosts' : gosts,
#                               },
#                               context_instance=RequestContext(request), )


# @cache_page(settings.CACHE_TIME_BASE_VIEW)
# def show_gost(request, gost_slug=None, template_name="marka_gost/gost.html"):

#     current_menu = MenuCatalog.objects.get(id=settings.ID_MENU_MARKA_GOST)
#     oneGost = GOST.objects.get(number_lat=gost_slug)
#     gostHead = GOSTHead.objects.get(id=oneGost.position.position_id)
#     gostGroup = GOSTGroup.objects.get(id=oneGost.position_id)
#     MetallCatalogGost= Product.objects.filter(gost=oneGost.id, isHidden=False)[:settings.PRODUCTS_PER_PAGE]

#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))



# GOST/views.py

from django.shortcuts import render, get_object_or_404 
from django.http import Http404
from django.views.decorators.cache import cache_page

from django.conf import settings 

from menu.models import MenuCatalog, Product
from .models import GOST, GOSTGroup, GOSTHead 
from cart.forms import ProductAddToCartForm
from cart import cartpy


def GostHeadV(request, menuId, gostHeadId):
    currentMenu = get_object_or_404(MenuCatalog, id=menuId)
    gostHead = get_object_or_404(GOSTHead, id=gostHeadId)
    gostGroups = GOSTGroup.objects.filter(position=gostHead)

    context = {
        'currentMenu': currentMenu,
        'oneGostHead': gostHead,
        'gostGroups': gostGroups,
    }
    return render(request, 'index.html', context)


def GostGroupV(request, menuId, gostHeadId, gostGroupId):
    currentMenu = get_object_or_404(MenuCatalog, id=menuId)
    gostHead = get_object_or_404(GOSTHead, id=gostHeadId)
    gostGroup = get_object_or_404(GOSTGroup, id=gostGroupId)
    gosts = GOST.objects.filter(position=gostGroup)

    context = {
        'currentMenu': currentMenu,
        'oneGostHead': gostHead,
        'oneGostGroup': gostGroup,
        'gosts': gosts,
    }
    return render(request, 'index.html', context)


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def show_gost(request, gost_slug=None, template_name="marka_gost/gost.html"):
    current_menu = get_object_or_404(MenuCatalog, id=settings.ID_MENU_MARKA_GOST)
    
    oneGost = get_object_or_404(GOST, number_lat__iexact=gost_slug)
    
    gostGroup = oneGost.position
    gostHead = gostGroup.position

    MetallCatalogGost = Product.objects.filter(gost=oneGost, isHidden=False)[:settings.PRODUCTS_PER_PAGE]

    context = {
        'current_menu': current_menu,
        'oneGost': oneGost,
        'gostHead': gostHead,
        'gostGroup': gostGroup,
        'MetallCatalogGost': MetallCatalogGost,
    }
    return render(request, template_name, context)
