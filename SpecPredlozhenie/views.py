# -*- coding: utf-8 -*-
from SpecPredlozhenie.models import SpecPredlozhenie
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core import urlresolvers
from menu.models import MenuCatalog
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token

import pkfcvet.settings as settings


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def show_specpredlozhenie(request, specpredl_slug=None, template_name="sys/specpredlozhenie.html"):

    if specpredl_slug:
        specpredl_one = get_object_or_404(SpecPredlozhenie, name_lat=specpredl_slug)

    specpredl_list = SpecPredlozhenie.objects.filter(isHidden=False)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))