# -*- coding: utf-8 -*-
from photogallery.models import Photogallery
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token
import pkfcvet.settings as settings

from menu.models import MenuCatalog

SLUG_PAGE_PHOTO = "photogallery"


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def photogallery_all(request, page=0, template_name="info/photogallery.html"):
    try:
        page = int(page)
    except:
        raise Http404()
    SIZE_PAGE_PHOTO = 80
    URL_PAGE_PHOTO = "/photogallery/"
    current_menu = get_object_or_404(MenuCatalog, slug=SLUG_PAGE_PHOTO)
    photogallery_list = Photogallery.objects.filter(isHidden=False)

    paginatorMin = 1
    paginatorMax = 5
    paginator = Paginator(photogallery_list, SIZE_PAGE_PHOTO)

    if page == 1 or page > paginator.num_pages:
        return HttpResponseRedirect(URL_PAGE_PHOTO)
    if page == 0:
        page = 1

    try:
        photogallery_list = paginator.page(page)

        if int(page) < 5:
            paginatorMin = 1
            paginatorMax = 5
        else:
            paginatorMin = max(int(page)-2,1)
            paginatorMax = min(int(page)+2,paginator.num_pages)

    except PageNotAnInteger:
        photogallery_list = paginator.page(1)

    except EmptyPage:
        photogallery_list = paginator.page(paginator.num_pages)

    return render(request, template_name, locals())

