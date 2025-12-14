# -*- coding: utf-8 -*-
from portfolio.models import Portfolio
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
# from django.core import urlresolvers
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token
import pkfcvet.settings as settings


@cache_page(settings.CACHE_TIME_BASE_VIEW)
def show_portfolio(request, portfolio_slug, template_name="sys/portfolio.html"):

    portfolio_one = get_object_or_404(Portfolio, name_lat=portfolio_slug)
    portfolio_list = Portfolio.objects.filter(isHidden=False)

    return render(request, template_name, locals())