# -*- coding: utf-8 -*-
from headers import *
from robots.models import RobotsTxt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from menu.views_form import get_current_filial

def RobotsV(request):

    #Формирование текстовых блоков для выбранного региона
    filials = Filials.objects.filter(isHidden=False)
    #определение на каком url будет пользователь (для корректного перехода между городами)
    host = request.get_host()
    # анализ поддомена и выбор города
    # current_filial = None
    # if filials:
    #     current_filial = filials[0]
    # for item in filials:
    #     if item.subdomain_name in host:
    #         current_filial = item
    current_filial = get_current_filial(host)

    try:
        robots_txt = RobotsTxt.objects.get(filial=current_filial.id).text
    except:
        robots_txt=""

    return render_to_response('robots.html', {
        'robots_txt': robots_txt,
    },
    context_instance=RequestContext(request), )