# -*- coding: utf-8 -*-
from Sertificats.models import Sertificats
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core import urlresolvers
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token

from menu.models import MenuCatalog
import pkfcvet.settings as settings

SLUG_PAGE_SERT = "sertificats"


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def sertficats_all(request, page=0, template_name="info/sertificates.html"):
    try:
        page = int(page)
    except:
        raise Http404()
    SIZE_PAGE_SERT = 8
    URL_PAGE_SERT = "/sertificats/"
    current_menu = get_object_or_404(MenuCatalog, slug=SLUG_PAGE_SERT)
    sertificats_list = Sertificats.objects.filter(isHidden=False)

    paginatorMin = 1
    paginatorMax = 5
    paginator = Paginator(sertificats_list, SIZE_PAGE_SERT)

    if page == 1 or page > paginator.num_pages:
        return HttpResponseRedirect(URL_PAGE_SERT)
    if page == 0:
        page = 1

    try:
        sertificats_list = paginator.page(page)

        if int(page) < 5:
            paginatorMin = 1
            paginatorMax = 5
        else:
            paginatorMin = max(int(page)-2,1)
            paginatorMax = min(int(page)+2,paginator.num_pages)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sertificats_list = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sertificats_list = paginator.page(paginator.num_pages)

    return render(request, template_name, locals())

