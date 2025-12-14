# -*- coding: utf-8 -*-
import os
import datetime
from django.db.models import Q, Prefetch
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponsePermanentRedirect
# from django.core import urlresolvers
from django.conf import settings
from cart import cartpy
from cart.forms import ProductAddToCartForm
from stats import statspy as stats
from Contacts.models import Contacts
from menu.models import Product

from menu.models import MenuCatalog
from Filials.models import Filials
from cart import cartpy as cart
from checkout.forms import CheckoutForm
from checkout import checkoutpy as checkout
from django.views.decorators.csrf import csrf_exempt

from robots.models import RobotsTxt
from Pricelists.models import PricelistsMain
from menu.views_form import get_current_filial
from TextBlockUrl.models import TextBlockUrl


from django.http import JsonResponse
from django.views import View
import requests

# --- NOUVEAUX IMPORTS ---
from checkout.forms import CheckoutForm # Assurez-vous que ce chemin est correct
from checkout.models import Order
from checkout.checkoutpy import task_send_mail_order
# --- FIN DES NOUVEAUX IMPORTS ---


MAX_COUNT_PRODUCTS = 500000


def global_views(request):
    """
    Context processor final, avec débogage et stratégie de requête en 2 étapes
    pour forcer le pré-chargement des relations 'parent'.
    """
    
    # --- 1. Données spécifiques à la requête ---
    host = request.get_host()
    current_filial = get_current_filial(host)
    cart_item_count = cartpy.cart_distinct_item_count(request)
    recently_viewed = stats.get_recently_viewed(request)

    # --- 2. NOUVELLE STRATÉGIE DE REQUÊTE OPTIMISÉE ---
    
    # Étape A: Récupérer les IDs de tous les menus pertinents
    menu_ids = list(MenuCatalog.objects.filter(
        Q(parent=None, isHidden=False) |
        Q(comment__in=["SPEC", "TOP_AND_FOOTER_RIGHT", "FOOTER_LEFT", "FOOTER_RIGHT"], isHidden=False)
    ).values_list('id', flat=True))
    
    # Étape B: Construire le queryset final en filtrant par ces IDs et en forçant le select_related
    relations_a_precharger = ['typeMenu', 'parent', 'parent__parent', 'parent__parent__parent']
    
    all_menus = MenuCatalog.objects.filter(id__in=menu_ids).select_related(*relations_a_precharger)
    
    # --- 3. Traitement en Python (sur la base des données pré-chargées) ---

    # Matérialiser le queryset en une liste pour l'inspecter et le réutiliser
    all_menus_list = list(all_menus)
    
    # --- DÉBOGAGE ---
    # print("\n--- DÉBOGAGE global_views (stratégie en 2 étapes) ---")
    # print(f"IDs des menus à charger: {menu_ids}")
    # print(f"Nombre total de menus chargés par la requête principale: {len(all_menus_list)}")
    
    main_menus = [m for m in all_menus_list if m.parent is None and m.comment == ""]
    
    specpredlozhenie_menu_qs = [m for m in all_menus_list if m.comment == "SPEC"]
    
    top_menu_items_raw = [m for m in all_menus_list if m.comment == "TOP_AND_FOOTER_RIGHT"]
    
    # --- DÉBOGAGE SPÉCIFIQUE POUR top_menu ---
    # print(f"\n--- DÉBOGAGE top_menu ---")
    # print(f"Nombre d'éléments bruts pour top_menu: {len(top_menu_items_raw)}")
    # print("Vérification du pré-chargement des parents pour les éléments de top_menu:")
    for item in top_menu_items_raw:
        is_parent_cached = "N/A" # Si pas de parent
        if item.parent:
            try:
                # La méthode is_cached peut être peu fiable, on teste directement.
                # Cet accès ne devrait déclencher AUCUNE requête si le pré-chargement a fonctionné.
                _ = item.parent.name 
                is_parent_cached = True
            except Exception as e:
                 # Si une erreur se produit, le pré-chargement a échoué
                 is_parent_cached = f"False (Erreur: {e})"
        # print(f"  - ID: {item.id}, Nom: '{item.name}', Parent ID: {item.parent_id}, Parent pré-chargé: {is_parent_cached}")

    top_menu = sorted(
        top_menu_items_raw,
        key=lambda m: m.order_number or float('inf')
    )
    
    # print(f"Nombre d'éléments dans top_menu (après tri): {len(top_menu)}")
    # print("--- FIN DÉBOGAGE ---\n")

    # Le reste de la logique de construction des menus
    footer_left_menu_items = [m for m in main_menus if m.typeMenu and m.typeMenu.name == "Каталог"]
    footer_left_menu_items.extend([m for m in all_menus_list if m.comment == "FOOTER_LEFT"])
    footer_left_menu_items.extend(specpredlozhenie_menu_qs)
    
    footer_right_menu_items = list(main_menus)
    footer_right_menu_items.extend([m for m in all_menus_list if m.comment == "FOOTER_RIGHT"])
    footer_right_menu_items.extend(top_menu)
    
    main_menus_catalog = [m for m in main_menus if (m.typeMenu and m.typeMenu.name == "Каталог") or m.name == "Производство"][:5]

    # --- 4. Le reste des requêtes (inchangé) ---
    contacts = Contacts.objects.first()
    filials = Filials.objects.filter(isHidden=False)
    pricelists_main_qs = PricelistsMain.objects.filter(isHidden=False)
    usluga_main_list = Product.objects.filter(catalog__name="Услуги", isHidden=False)[:4]
    proizvodsctvo_main_list = Product.objects.filter(catalog__name="Производство", isHidden=False)[:4]

    # --- 5. Construction du contexte final (inchangé) ---
    context = {
        'current_year': datetime.date.today().year,
        'start_year': settings.START_YEAR,
        'version_name': settings.VERSION_NAME,
        
        'request': request,
        'current_filial': current_filial,
        'cart_item_count': cart_item_count,
        'recently_viewed': recently_viewed,
        'cart_items': cart.get_cart_items(request),
        'current_url': f"{host}{request.path}",

        'contacts': contacts,
        'filials': filials,
        'main_menus': main_menus,
        'main_menus_catalog': main_menus_catalog,
        'specpredlozhenie_menu': specpredlozhenie_menu_qs[0] if specpredlozhenie_menu_qs else None,
        'top_menu': top_menu,
        'footer_left_menu': list(set(footer_left_menu_items)),
        'footer_right_menu': list(set(footer_right_menu_items)),
        'pricelist_main': pricelists_main_qs.first(),
        'opros_main': pricelists_main_qs[1] if len(pricelists_main_qs) > 1 else None,
        'usluga_main_list': usluga_main_list,
        'proizvodsctvo_main_list': proizvodsctvo_main_list,
    }
    
    return context


def RobotsV(request):
    # Récupération de la filiale actuelle
    host = request.get_host()
    current_filial = get_current_filial(host)

    robots_txt_content = ""
    
    if current_filial:
        try:
            robots_txt_obj = RobotsTxt.objects.get(filial=current_filial)
            robots_txt_content = robots_txt_obj.text
        except RobotsTxt.DoesNotExist:
            pass

    if "test." in host:
        robots_txt_content = ""
    return HttpResponse(robots_txt_content, content_type="text/plain")




def get_today():
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M")


# @csrf_exempt
# def OrderPhone(request):
#     """
#     Заказ звонка.
#     """
#     from checkout.models import Order
#     from checkout.checkoutpy import task_send_mail_order

#     name = u'Клиент'
#     phone = ""
#     email = ""
#     text = ""
#     robot = ""
#     info_filial_id = ""
#     ip_user = request.META['REMOTE_ADDR']

#     date = get_today()
#     consent = False
#     consent_2 = False
#     try:
#         consent = request.POST['consent']
#     except:
#         pass
#     try:
#         consent_2 = request.POST['consent_2']
#     except:
#         pass
#     if request.POST['phone']:
#         phone = request.POST['phone']
#     try:
#         if request.POST['email']:
#             email = request.POST['email']
#     except:
#         email = None
#     try:
#         if request.POST['text']:
#             text = request.POST['text']
#     except:
#         text = None

#     if request.POST['robot']:
#         robot = request.POST['robot']
#     if text != u"Заказ рассылки":
#         if len(phone) >= 10 and robot == "" and consent and consent_2 and text:
#             order = Order()
#             checkout_form = CheckoutForm(request.POST, instance=order)
#             if checkout_form.is_valid():
#                 order = checkout_form.save(commit=False)
#             order.transaction_id = 0
#             order.ip_address = request.META.get('REMOTE_ADDR')
#             order.user = None
#             text_order = ""
#             try:
#                 text_order = ' Комментарий: ' + request.POST['text_zayavka'] + "\n"
#             except:
#                 pass
#             if order.text == u"Заказ рассылки":
#                 pass
#             elif order.text:
#                 order.text = u"Заказ звонка по '" + order.text + u"'" + text_order
#             else:
#                 order.text = u"Заказ звонка;" + text_order
#             # tmp = Order(name=name, phone=phone, email="", text="", transaction_id=0, user=None, comment=u"Заказ звонка", date=date, ip_address=ip_user)
#             current_filial = get_current_filial(request.get_host())
#             order.address_to = current_filial.email
#             if request.session.get(settings.CONTACTS_SESSION_KEY, '') == 'yclid':
#                 if current_filial.email_yclid:
#                     order.address_to = current_filial.email_yclid
#             if request.session.get(settings.CONTACTS_SESSION_KEY, '') == 'gclid':
#                 if current_filial.email_gclid:
#                     order.address_to = current_filial.email_gclid
#             order.save()

#             #Roistat Send Start
#             try:
#                 import urllib
#                 import urllib2

#                 roistat_data = {
#                     'roistat': request.COOKIES.get('roistat_visit'),
#                     'key': 'ODNiNmJjODU1ZmY5Mzc5Nzg2M2I5NTliODdkNjBiYWI6MjI1NDcw',
#                     'sync': '0',
#                     'is_skip_sending': '0',
#                     'title': 'Заказ звонка',
#                     'phone': phone.encode('utf8'),
#                     'name': str(request.POST['name']).encode('utf8'),
#                     'comment': str(request.POST['text_zayavka']).encode('utf8'),
#                     'fields[UF_CRM_62CC22E9F3BED]': '{visit}',
#                     'fields[UF_CRM_1665139612]': '{landingPage}',
#                     'fields[UF_CRM_1665139637]': request.META['HTTP_HOST'],
#                     'fields[UF_CRM_1665139679]': '{source}',
#                     'fields[UF_CRM_1665139714]': '{city}',
#                     'fields[UTM_CAMPAIGN]': '{utmCampaign}',
#                     'fields[UTM_CONTENT]': '{utmContent}',
#                     'fields[UTM_MEDIUM]': '{utmMedium}',
#                     'fields[UTM_SOURCE]': '{utmSource}',
#                     'fields[UTM_TERM]': '{utmTerm}',
#                     'fields[STAGE_ID]': 'FINAL_INVOICE'
#                 }
#                 if email != None:
#                     roistat_data['email'] = email.encode('utf8'),

#                 file = open('roistat_data.json', 'w')
#                 file.write(str(roistat_data))
#                 file.close()

#                 data = urllib.urlencode(roistat_data)
#                 url = 'https://cloud.roistat.com/api/proxy/1.0/leads/add'
#                 req = urllib2.Request(url, data)
#                 response = urllib2.urlopen(req)

#                 # add response to log

#                 file = open('roistat_response.log', 'w')
#                 file.write(response.read())
#                 file.close()
#             except Exception as e:
#                 import traceback
#                 logf = open("roistat_send_error.log", "w")
#                 logf.write(str(traceback.format_exc()))
#             #Roistat Send End

#             task_send_mail_order(request, order)
#         else:
#             return 1
#     else:
#         if email and robot == "" and consent and consent_2:
#             order = Order()
#             checkout_form = CheckoutForm(request.POST, instance=order)
#             if checkout_form.is_valid():
#                 order = checkout_form.save(commit=False)
#             order.transaction_id = 0
#             order.ip_address = request.META.get('REMOTE_ADDR')
#             order.user = None
#             text_order = ""
#             try:
#                 text_order = ' Комментарий: ' + request.POST['text_zayavka'] + "\n"
#             except:
#                 pass
#             if order.text == u"Заказ рассылки":
#                 pass
#             elif order.text:
#                 order.text = u"Заказ звонка по продукту '" + order.text + u"'" + text_order
#             else:
#                 order.text = u"Заказ звонка. " + text_order
#             current_filial = get_current_filial(request.get_host())
#             order.address_to = current_filial.email
#             if request.session.get(settings.CONTACTS_SESSION_KEY, '') == 'yclid':
#                 if current_filial.email_yclid:
#                     order.address_to = current_filial.email_yclid
#             if request.session.get(settings.CONTACTS_SESSION_KEY, '') == 'gclid':
#                 if current_filial.email_gclid:
#                     order.address_to = current_filial.email_gclid
#             order.save()
#             task_send_mail_order(request, order)
#         else:
#             return 1

#     return HttpResponse(0)


class SendFormOrder(View):
    """
    Vue moderne qui utilise le CheckoutForm existant.
    """
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)

        if not form.is_valid():
            # Retourner une erreur claire si les données ne sont pas valides
            # Les messages d'erreur seront en russe, comme défini dans le formulaire.
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
        
        # Les données sont valides, on peut créer l'objet Order
        order = form.save(commit=False)
        
        # Données supplémentaires qui ne viennent pas du formulaire
        order.ip_address = request.META.get('REMOTE_ADDR')
        
        # Construire le champ 'text'
        form_type = form.cleaned_data.get('text', '')
        comment = form.cleaned_data.get('text_zayavka', '')

        if form_type == "Заказ рассылки":
            order.text = form_type
        else:
            order.text = f"Заказ звонка по '{form_type}'" if form_type else "Заказ звонка"
            if comment:
                order.text += f" Комментарий: {comment}"

        # Gérer la logique de la filiale
        current_filial = get_current_filial(request.get_host())
        order.address_to = current_filial.email
        contact_type = request.session.get(settings.CONTACTS_SESSION_KEY, '')
        if contact_type == 'yclid' and current_filial.email_yclid:
            order.address_to = current_filial.email_yclid
        elif contact_type == 'gclid' and current_filial.email_gclid:
            order.address_to = current_filial.email_gclid
            
        order.save()

        # Envoyer les données à Roistat et l'email de notification
        self.send_to_roistat(request, order, form.cleaned_data)
        task_send_mail_order(request, order)

        return JsonResponse({'status': 'success', 'message': 'Заявка успешно отправлена!'})

    def send_to_roistat(self, request, order, data):
        roistat_data = {
            'roistat': request.COOKIES.get('roistat_visit'),
            'key': settings.ROISTAT_API_KEY, # Mettez votre clé dans settings.py !
            'title': 'Заказ звонка',
            'phone': order.phone,
            'name': order.name,
            'comment': data.get('text_zayavka', ''),
            'email': order.email,
        }
        
        try:
            url = 'https://cloud.roistat.com/api/proxy/1.0/leads/add'
            response = requests.post(url, data=roistat_data, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Utilisez le logger de Django pour une meilleure gestion des erreurs
            logger.error(f"Erreur lors de l'envoi à Roistat: {e}")


def clear_session(request):
    from cart.models import CartItem
    CartItem.objects.all().delete()
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()
    return HttpResponseRedirect("/")


def __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time):
    os.system("cd www;rm " + name + ".gz;gzip " + name)
    fs.write(
        '<sitemap>\n<loc>{}://{}{}/{}.gz</loc>\n<lastmod>{}</lastmod>\n</sitemap>\n'.format(scheme, subdomain_txt, host,
                                                                                            name, str(time)))


def sitemap_gen_long(scheme, host):
    from catalog_filter.models import CatalogFilterValue
    MAX_ITEM_IN_FILE = 50000

    filials_map_list = Filials.objects.filter(isHidden=False)

    category_list = MenuCatalog.objects.filter(isHidden=False)
    prod_list = Product.objects.filter(isHidden=False).only('slug')[:MAX_COUNT_PRODUCTS]
    # prod_list1 = Product.objects.filter(isHidden=False).only('slug')[:MAX_COUNT_PRODUCTS]
    # prod_list2 = Product.objects.filter(isHidden=False).only('slug')[MAX_COUNT_PRODUCTS:2 * MAX_COUNT_PRODUCTS]
    # prod_list3 = Product.objects.filter(isHidden=False).only('slug')[2 * MAX_COUNT_PRODUCTS:]
    text_block_url_list = TextBlockUrl.objects.filter(isHidden=False)

    for item_filial in filials_map_list:
        if "." in item_filial.subdomain_name:
            name_sitemap_index = 'sitemap_' + item_filial.subdomain_name.replace(".", "") + '.xml'
        else:
            name_sitemap_index = 'sitemap.xml'

        fs = open(("www/" + name_sitemap_index), 'w')
        fs.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        item_count = 0
        file_count = 1
        subdomain_txt = ""
        time = datetime.datetime.now().strftime("%Y-%m-%d")

        # --- Генерация sitemap для урл ---
        if "." in item_filial.subdomain_name:
            name = 'sitemap_marki_' + item_filial.subdomain_name.replace(".", "") + '_' + str(file_count) + '.xml'
            subdomain_txt = item_filial.subdomain_name
        else:
            name = 'sitemap_marki_' + str(file_count) + '.xml'

        f = open(("www/" + name), 'w')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')

        for item in text_block_url_list:
            f.write('<url>\n')
            f.write(('<loc>') + ((scheme + '://' + subdomain_txt + host) + str(item.url)) + ('</loc>\n'))
            f.write(('<lastmod>') + str(time) + ('</lastmod>\n'))
            # f.write('<changefreq>weekly</changefreq>\n')
            f.write('<priority>0.9</priority>\n')
            f.write('</url>\n')
            item_count += 1
            if item_count >= MAX_ITEM_IN_FILE:
                f.write('</urlset>')
                f.close()
                __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time)
                file_count += 1
                item_count = 0
                if "." in item_filial.subdomain_name:
                    name = 'sitemap_marki_' + item_filial.subdomain_name.replace(".", "") + '_' + str(
                        file_count) + '.xml'
                else:
                    name = 'sitemap_marki_' + str(file_count) + '.xml'
                f = open(("www/" + name), 'w')
                f.write(
                    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
        f.write('</urlset>')
        f.close()
        __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time)
        # ---------------------------------
        item_count = 0
        file_count = 1

        if "." in item_filial.subdomain_name:
            name = 'sitemap_' + item_filial.subdomain_name.replace(".", "") + '_' + str(file_count) + '.xml'
            subdomain_txt = item_filial.subdomain_name
        else:
            name = 'sitemap_' + str(file_count) + '.xml'

        f = open(("www/" + name), 'w')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')

        for item in category_list:
            f.write('<url>\n')
            f.write(('<loc>') + ((scheme + '://' + subdomain_txt + host + '/') + str(item.slug)) + ('/</loc>\n'))
            f.write(('<lastmod>') + str(time) + ('</lastmod>\n'))
            # f.write('<changefreq>weekly</changefreq>\n')
            f.write('<priority>0.9</priority>\n')
            f.write('</url>\n')
            item_count += 1
            if item_count >= MAX_ITEM_IN_FILE:
                f.write('</urlset>')
                f.close()
                __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time)
                file_count += 1
                item_count = 0
                if "." in item_filial.subdomain_name:
                    name = 'sitemap_' + item_filial.subdomain_name.replace(".", "") + '_' + str(file_count) + '.xml'
                else:
                    name = 'sitemap_' + str(file_count) + '.xml'
                f = open(("www/" + name), 'w')
                f.write(
                    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')

            filter_list_marka = CatalogFilterValue.objects.filter(category=item, filter_name__name_lat="marka",
                                                                  is_hidden=False)
            for sub_item in filter_list_marka:
                try:
                    f.write(('<url>\n<loc>') + ((
                                                            scheme + '://' + subdomain_txt + host + '/') + item.slug + '/' + sub_item.value_lat) + (
                                '/</loc>\n'))
                    f.write(('<lastmod>') + str(time) + ('</lastmod>\n'))
                    # f.write('<changefreq>weekly</changefreq>\n')
                    f.write('<priority>0.9</priority>\n')
                    f.write('</url>\n')
                    item_count += 1
                except:
                    continue

                if item_count >= MAX_ITEM_IN_FILE:
                    f.write('</urlset>')
                    f.close()
                    __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time)
                    file_count += 1
                    item_count = 0
                    if "." in item_filial.subdomain_name:
                        name = 'sitemap_' + item_filial.subdomain_name.replace(".", "") + '_' + str(file_count) + '.xml'
                    else:
                        name = 'sitemap_' + str(file_count) + '.xml'
                    f = open(("www/" + name), 'w')
                    f.write(
                        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
        for item in prod_list:
            try:
                f.write(('<url>\n<loc>') + ((scheme + '://' + subdomain_txt + host + '/product/') + item.slug) + (
                    '/</loc>\n'))
            except:
                continue
            f.write(('<lastmod>') + str(time) + ('</lastmod>\n'))
            # f.write('<changefreq>weekly</changefreq>\n')
            f.write('<priority>0.8</priority>\n')
            f.write('</url>\n')
            item_count += 1
            if item_count >= MAX_ITEM_IN_FILE:
                f.write('</urlset>')
                f.close()
                __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time)
                file_count += 1
                item_count = 0
                if "." in item_filial.subdomain_name:
                    name = 'sitemap_' + item_filial.subdomain_name.replace(".", "") + '_' + str(file_count) + '.xml'
                else:
                    name = 'sitemap_' + str(file_count) + '.xml'
                f = open(("www/" + name), 'w')
                f.write(
                    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
        f.write('</urlset>')
        f.close()
        __sitemap_gen_end(fs, scheme, subdomain_txt, host, name, time)

        fs.write('</sitemapindex>')
        fs.close()


def sitemap_gen(request):
    import threading
    t = threading.Thread(target=sitemap_gen_long, args=[request.scheme, request.get_host(), ])
    t.setDaemon(True)
    t.start()
    return HttpResponsePermanentRedirect("/")


def catalog_update(request):
    catalog_list = MenuCatalog.objects.filter(isHidden=False)
    for item in catalog_list:
        item.save()
    return HttpResponsePermanentRedirect("/")
