# -*- coding: utf-8 -*-

#----------
import xlrd
import xlwt
import sys
import glob
import os
import codecs
import locale
import datetime
import subprocess
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from menu.models import MenuCatalog, Product, tableProductDop, ProductUsluga


#  форма, выбора, что экспортировать
def ExportViews(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/admin/')
    category = MenuCatalog.objects.filter(typeMenu__name="Каталог")
    context = {
        'category': category,
    }
    return render(request, 'export/export_index.html', context)



def ExportCatalog(request):
    if not request.user.is_authenticated:
       return redirect('/admin/')
    
    dic = {'name': '', 'link': ''}

    if 'select_type' in request.POST:
        dic = CatalogNewExport(request, request.POST['select_type'])
    context = {
        'name': dic['name'],
        'link': dic['link']
    }
    return render(request, 'export/export_download.html', context)


# экспорт
def CatalogNewExport(request, select_type=None, page=None):
    MetallCatalog2 = Product.objects.filter(catalog=select_type, isHidden=False)
    currentCategory = MenuCatalog.objects.get(id=select_type)
    w = xlwt.Workbook(style_compression=2)
    ws = w.add_sheet(u'Прайс')

    HEAD_COLOR = 67

    class Cell(object):
        """__init__() functions as the class constructor"""
        def __init__(self, data=None, color=int()):
            self.data = data
            self.color = color

        def getData(self):
            return self.data

        def getColor(self):
            return self.color

    #header = 0
    # запись в файл options.out.

    # list_row2 = []
    #
    # list_row2.append([Cell(u'Наименование', HEAD_COLOR), Cell(u'Размер, мм', HEAD_COLOR), Cell(u'ГОСТ, ОСТ, ТУ', HEAD_COLOR),
    #                   Cell(u'Марка стали', HEAD_COLOR), Cell(u'Описание', HEAD_COLOR), Cell(u'Цена, руб/тн', HEAD_COLOR)])
    i=0

    style_date = xlwt.easyxf("pattern: pattern solid; alignment: wrap True, vertical top, horizontal left; border: left thin, right thin, top thin, bottom thin;", num_format_str='DD.MM.YYYY')
    # style_date.pattern.pattern_fore_colour = Cell(u'', 1).color
    ws.write(i, 0, Cell(u"ID товара", HEAD_COLOR).data, style_date)
    ws.write(i, 1, Cell(u"Приоритет",HEAD_COLOR).data, style_date)
    ws.write(i, 2, Cell(u'Наименование товара', HEAD_COLOR).data, style_date)
    ws.write(i, 3, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 4, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 5, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 6, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 7, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 8, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 9, Cell(u'Размер, мм', HEAD_COLOR).data, style_date)
    ws.write(i, 10, Cell(u'Марка стали', HEAD_COLOR).data, style_date)
    ws.write(i, 11, Cell(u'ГОСТ, ОСТ, ТУ', HEAD_COLOR).data, style_date)
    ws.write(i, 12, Cell(u'Наличие', HEAD_COLOR).data, style_date)
    ws.write(i, 13, Cell(u'Цена, руб.', HEAD_COLOR).data, style_date)
    ws.write(i, 14, Cell(u'Единица измерения', HEAD_COLOR).data, style_date)
    ws.write(i, 15, Cell(u'Фото товара 1', HEAD_COLOR).data, style_date)
    ws.write(i, 16, Cell(u'Фото товара 2', HEAD_COLOR).data, style_date)
    ws.write(i, 17, Cell(u'Описание товара', HEAD_COLOR).data, style_date)
    ws.write(i, 18, Cell(u'Производитель', HEAD_COLOR).data, style_date)
    ws.write(i, 19, Cell(u'Страна производителя', HEAD_COLOR).data, style_date)
    ws.write(i, 20, Cell(u'Способ изготовления', HEAD_COLOR).data, style_date)
    ws.write(i, 21, Cell(u"ID категории товара", HEAD_COLOR).data, style_date)
    ws.write(i, 22, Cell(u'Сертификат', HEAD_COLOR).data, style_date)
    ws.write(i, 23, Cell(u'Доп. товар', HEAD_COLOR).data, style_date)
    ws.write(i, 24, Cell(u'Доп. товар', HEAD_COLOR).data, style_date)
    ws.write(i, 25, Cell(u'Доп. товар', HEAD_COLOR).data, style_date)
    ws.write(i, 26, Cell(u'Доп. товар', HEAD_COLOR).data, style_date)
    ws.write(i, 27, Cell(u'Услуга', HEAD_COLOR).data, style_date)
    ws.write(i, 28, Cell(u'Услуга', HEAD_COLOR).data, style_date)
    ws.write(i, 29, Cell(u'Услуга', HEAD_COLOR).data, style_date)
    ws.write(i, 30, Cell(u'Услуга', HEAD_COLOR).data, style_date)


    for item in MetallCatalog2:
        i = i + 1
        # if(round(i/10) == i/10.):
        #    print i
        description=""
        if (item.description):
            description=item.description

        marka=""
        if (item.marka_id):
            marka=item.marka

        gost=""
        if (item.gost_id):
            gost=item.gost
        # list_row2.append([Cell(unicode(item.type), 1), Cell(unicode(str(item.size_a)+"x"+str(item.size_b)+"x"+str(item.size_c)), 1), Cell(unicode(gost), 1),
        #              Cell(unicode(marka), 1), Cell(unicode(description), 1), Cell(unicode(item.price), 1)])
        style_date.pattern.pattern_fore_colour = Cell(unicode(item.catalog), 1).color
        ws.write(i, 0, Cell(unicode(item.id)+".0", 1).data, style_date)
        if item.order_number:
            ws.write(i, 1, Cell(unicode(item.order_number), 1).data, style_date)
        else:
            ws.write(i, 1, Cell("", 1).data, style_date)
        ws.write(i, 2, Cell(unicode(item.name_main), 1).data, style_date)
        # ws.write(i, 2, Cell(unicode(str(item.size_a)+"x"+str(item.size_b)+"x"+str(item.size_c)), 1).data, style_date)
        if item.size_a:
            ws.write(i, 3, Cell(unicode(item.size_a), 1).data, style_date)
        else:
            ws.write(i, 3, Cell("", 1).data, style_date)
        if item.size_b:
            ws.write(i, 4, Cell(unicode(item.size_b), 1).data, style_date)
        else:
            ws.write(i, 4, Cell("", 1).data, style_date)
        if item.size_c:
            ws.write(i, 5, Cell(unicode(item.size_c), 1).data, style_date)
        else:
            ws.write(i, 5, Cell("", 1).data, style_date)
        if item.size_d:
            ws.write(i, 6, Cell(unicode(item.size_d), 1).data, style_date)
        else:
            ws.write(i, 6, Cell("", 1).data, style_date)
        if item.size_e:
            ws.write(i, 7, Cell(unicode(item.size_e), 1).data, style_date)
        else:
            ws.write(i, 7, Cell("", 1).data, style_date)
        if item.size_f:
            ws.write(i, 8, Cell(unicode(item.size_f), 1).data, style_date)
        else:
            ws.write(i, 8, Cell("", 1).data, style_date)
        if item.size_l:
            ws.write(i, 9, Cell(unicode(item.size_l), 1).data, style_date)
        else:
            ws.write(i, 9, Cell("", 1).data, style_date)
        # if item.size_m:
        #     ws.write(i, 10, Cell(unicode(item.size_m), 1).data, style_date)
        # else:
        #     ws.write(i, 10, Cell("", 1).data, style_date)
        if item.marka:
            ws.write(i, 10, Cell(unicode(item.marka), 1).data, style_date)
        else:
            ws.write(i, 10, Cell("", 1).data, style_date)
        if item.gost:
            ws.write(i, 11, Cell(unicode(item.gost), 1).data, style_date)
        else:
            ws.write(i, 11, Cell("", 1).data, style_date)
        ws.write(i, 12, Cell(unicode(item.available), 1).data, style_date)
        ws.write(i, 13, Cell(unicode(item.price), 1).data, style_date)
        ws.write(i, 14, Cell(unicode(item.ed_izm), 1).data, style_date)
        ws.write(i, 15, Cell(request.get_host() + u"/media/"+unicode(item.image), 1).data, style_date)
        ws.write(i, 16, Cell(request.get_host() + u"/media/"+unicode(item.image_dop), 1).data, style_date)
        ws.write(i, 17, Cell(unicode(description), 1).data, style_date)
        ws.write(i, 18, Cell(unicode(item.vendor), 1).data, style_date)
        ws.write(i, 19, Cell(unicode(item.vendor_country), 1).data, style_date)
        ws.write(i, 20, Cell(unicode(item.method_of_manufacture), 1).data, style_date)
        ws.write(i, 21, Cell(unicode(item.catalog.id)+".0", 1).data, style_date)
        if item.sertificate:
            ws.write(i, 22, Cell(unicode(item.sertificate.id)+".0", 1).data, style_date)
        else:
            ws.write(i, 22, Cell("", 1).data, style_date)

        products_dop = tableProductDop.objects.filter(product=item)
        tmp_ind = 23
        for sub_item in products_dop[:4]:
            ws.write(i, tmp_ind, Cell(unicode(sub_item.product_dop.id)+".0", 1).data, style_date)
            tmp_ind += 1
        while tmp_ind<=26:
            ws.write(i, tmp_ind, Cell(unicode(""), 1).data, style_date)
            tmp_ind += 1

        usluga_product = ProductUsluga.objects.filter(product=item)
        tmp_ind = 27
        for sub_item in usluga_product[:4]:
            ws.write(i, tmp_ind, Cell(unicode(sub_item.usluga.id)+".0", 1).data, style_date)
            tmp_ind += 1
        while tmp_ind <= 30:
            ws.write(i, tmp_ind, Cell(unicode(""), 1).data, style_date)
            tmp_ind += 1


    #  создание файла
    today = datetime.date.today()
    d = today.strftime("%d_%m_%Y")
    id = str(currentCategory.id)
    name = id+"_"+d+".xls"

    #FIXME:  путь для Dev версии и рабочей отличается... пофиксить

    w.save("www/media/export/" + name)
    link = "/media/export/" + name

    return ({'link': link,
            'name': name,
            'order_number': 'order_number',
            })
