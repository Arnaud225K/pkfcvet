# -*- coding: utf-8 -*-
from menu.models import Product
from import_control.models import ImportControl
from django.http import HttpResponseRedirect


def import_control(curr_product):
    control_product_list = Product.objects.filter(slug=curr_product.slug)
    if len(control_product_list) > 0 and control_product_list[0].id != curr_product.id:
        import_error = ImportControl()
        import_error.slug = curr_product.slug
        import_error.dublicate_id = str(curr_product.id)
        import_error.original_id = str(control_product_list[0].id)
        import_error.info = str(curr_product)
        info_str = "Продукт: " + str(curr_product) + " \nзагружаемый в категорию: " + str(curr_product.catalog) + "\n"
        info_str += "латинское название (url): " + str(curr_product.slug) + " \nid: "+str(curr_product.id)+" \nдублирует:\n\n"
        for item in control_product_list:
            if item.id != curr_product.id:
                info_str += "продукт: " + str(item) + " \nкатегория: " + str(item.catalog)+" \nid: " + str(item.id) + "\n\n"
        import_error.result = info_str
        import_error.save()
        return False
    else:
        return True


def import_control_thread():
    product_list = Product.objects.all()
    i = 0
    result = []
    f = open(("www/ready"), 'w')
    f.write(str(i))
    f.close()
    for item in product_list:
        i = i + 1
        if not item.slug:
            item.set_slug()
            item.save()
        if i % 1000 == 0:
            f = open(("www/ready"), 'w')
            f.write(str(i))
            f.close()
        if item.slug in result:
            import_control(item)
            item.delete()
        result.append(item.slug)

    f = open(("www/ready"), 'w')
    f.write(str(i))
    f.write("END")
    f.close()


def import_control_url(request):
    import threading
    t = threading.Thread(target=import_control_thread)
    t.setDaemon(True)
    t.start()

    return HttpResponseRedirect("/")