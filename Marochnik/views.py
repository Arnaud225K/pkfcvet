# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from Marochnik.models import MarkaMetall, Metall,MetallGroup
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token
from menu.models import MenuCatalog, Product
from cart.forms import ProductAddToCartForm
from cart import cartpy
import pkfcvet.settings as settings


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def show_metall(request, metall_slug=None, template_name="marka_gost/marka_head.html"):
    current_menu = MenuCatalog.objects.get(id=settings.ID_MENU_MARKA_GOST)
    metall = Metall.objects.get(name_lat=metall_slug)
    metallGroups = MetallGroup.objects.filter(position=metall.id)

    return render(request, template_name, locals())


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def show_metall_group(request, metall_group_slug=None, template_name="marka_gost/marka_middle.html"):

    current_menu = MenuCatalog.objects.get(id=settings.ID_MENU_MARKA_GOST)
    metallGroup = MetallGroup.objects.get(name_lat=metall_group_slug)
    metall = Metall.objects.get(id=metallGroup.position_id)
    marka = metallGroup.get_list_marka_metall()

    return render(request, template_name, locals())


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def show_marka_metall(request, marka_metall_slug=None, template_name="marka_gost/marka.html"):
    oneMarka = MarkaMetall.objects.get(name_lat=marka_metall_slug)
    current_menu = MenuCatalog.objects.get(id=settings.ID_MENU_MARKA_GOST)
    metallGroup = MetallGroup.objects.get(name_lat=oneMarka.position.name_lat)
    metall = Metall.objects.get(name_lat=oneMarka.position.position.name_lat)

    MetallCatalogMarka = Product.objects.filter(marka=oneMarka, isHidden=False)[:settings.PRODUCTS_PER_PAGE]

    oneMetall = metall
    oneMetallGroup = metallGroup
    oneMarka = oneMarka
    return render(request, template_name, locals())


@csrf_exempt
def SearchMarka(request):
    """
    Поиск по марочнику
    """
    marocknik = request.POST["marocknik"]
    marka = MarkaMetall.objects.get(name=marocknik)
    result = {'success': True, 'name': marka.name, 'description': marka.description }
    return HttpResponse(json.dumps(result), content_type='application/json')