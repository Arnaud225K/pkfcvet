# -*- coding: utf-8 -*-
from headers import *


def TextBlockMenuV(request,offsetmenu,offset):
    try:
        offsetmenu = int(offsetmenu)
    except ValueError:
        raise Http404()
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    currentMenu = Menu.objects.get(id=offsetmenu)
    oneTextBlockMenu = TextBlockMenu.objects.get(id=offset)



    return render_to_response('index.html', {
                              'currentMenu': currentMenu,
                              'oneTextBlockMenu' : oneTextBlockMenu,
                              },
                              context_instance=RequestContext(request), )
