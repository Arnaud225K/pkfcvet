from django.http import HttpResponse, JsonResponse
from django.views import View
import json
import traceback
from transliterate import translit

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.urls import reverse
from cart.forms import ProductAddToCartForm
import re

from .models import Product, MenuCatalog
from checkout.forms import CheckoutForm
from checkout.models import Order
from checkout import checkoutpy as checkout
from cart import cartpy as cart
from django.conf import settings
from django.middleware.csrf import get_token 


def get_current_filial(current_host):
    """
    :param current_host: Хост
    :return:current_filial: Текущий филиал
     Функция определяет текущий филиал
    """
    from Filials.models import Filials
    current_filial = None
    try:
        current_filial = Filials.objects.all()[0]
        current_filial = Filials.objects.get(name='Екатеринбург')
    except:
        pass
    filials_all = Filials.objects.all()
    for item in filials_all:
        if item.subdomain_name and item.subdomain_name in current_host:
            current_filial = item
    return current_filial


def form_error_str(elem):
    """
    :param elem:
    :return:
     Функция формирует вывод информации об ошибках из элементов стандартной формы (elem) для выдачи при запросе через Ajax
    """
    result_str = ""
    if elem.errors:
        result_str = '*' + elem.label + ': ' + elem.errors[0]
    return result_str


class CartCountView(View):
    """
    Retourne des informations dynamiques (panier, contacts) au format JSON.
    """
    def get(self, request):
        request.session.set_test_cookie()

        current_filial = get_current_filial(request.get_host())
        
        phone_to_display = current_filial.phone
        email_to_display = current_filial.email

        traffic_source = request.session.get(settings.CONTACTS_SESSION_KEY, '')

        if traffic_source == 'yclid':
            phone_to_display = current_filial.phone_yclid or phone_to_display
            email_to_display = current_filial.email_yclid or email_to_display
        elif traffic_source == 'gclid':
            phone_to_display = current_filial.phone_gclid or phone_to_display
            email_to_display = current_filial.email_gclid or email_to_display
        
        response_data = {
            'cart_item_count': cart.cart_distinct_item_count(request),
            'csrf_token': get_token(request),
            'phone_xclid': phone_to_display,
            'email_xclid': email_to_display,
        }

        return JsonResponse(response_data)



def slugify_filter_value(value):
    """
    Nettoie et "slugifie" une valeur de filtre pour l'URL.
    Remplace les virgules et les points par des tirets.
    """
    if not value:
        return ""
    
    # Remplacer la virgule par un point pour la translitération
    value_str = str(value).replace(',', '.')
    
    # Translitérer les caractères cyrilliques
    slug_base = translit(value_str, "ru", reversed=True)
    
    # Remplacer tout ce qui n'est pas une lettre, un chiffre ou un point par un tiret
    # Ensuite, remplacer le point par un tiret
    slug = re.sub(r'[^\w.]+', '-', slug_base).replace('.', '-').lower()
    
    # Supprimer les tirets en début/fin de chaîne
    return slug.strip('-')


class GetFilterUrl(View):
    """
    Construit une URL de catalogue filtrée PROPRE, sans valeurs "None".
    """
    def post(self, request, *args, **kwargs):
        menu_slug = request.POST.get('menu_slug')
        if not menu_slug:
            return JsonResponse({'error': 'menu_slug manquant'}, status=400)

        # 1. Collecter toutes les paires clé/valeur non vides
        filter_pairs = []
        
        # Carte des filtres à construire
        # (nom_formulaire, nom_url)
        filters_to_process = [
            ('filter_marka', 'marka'),
            ('filter_gost', 'gost'),
            ('filter_s1', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeAslug') or 's1').lower()),
            ('filter_s2', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeBslug') or 's2').lower()),
            ('filter_s3', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeCslug') or 's3').lower()),
            ('filter_s4', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeDslug') or 's4').lower()),
            ('filter_s5', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeEslug') or 's5').lower()),
            ('filter_s6', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeFslug') or 's6').lower()),
            ('filter_s7', (getattr(MenuCatalog.objects.get(slug__iexact=menu_slug), 'labelSizeLslug') or 's7').lower()),
        ]

        for form_name, url_key in filters_to_process:
            value = request.POST.get(form_name)
            
            # --- LA CONDITION CRUCIALE ---
            # On ajoute le filtre seulement si la valeur existe (n'est ni None, ni "")
            if value:
                # La valeur est déjà un slug (_lat), pas besoin de slugify
                filter_pairs.append(f"{url_key}={value}")

        # 2. Construire la nouvelle URL
        if filter_pairs:
            filters_str = "/".join(filter_pairs)
            # On utilise reverse pour construire l'URL proprement
            new_url = reverse('menu:menu_catalog_filtered', kwargs={
                'menu_slug': menu_slug,
                'filters_str': filters_str
            })
        else:
            new_url = reverse('menu:menu_catalog_detail', kwargs={'menu_slug': menu_slug})
        
        return JsonResponse({'url': new_url})




# class SendFormOrder(View):
#     """
#     Classe qui gère les soumissions de formulaires AJAX (panier, commande, demande de prix).
#     """

#     def _send_to_roistat(self, request, order, title_prefix=""):
#         """
#         Méthode privée pour envoyer les données à Roistat.
#         Factorisée pour éviter la duplication de code.
#         """
#         try:
#             order_text = order.text if order.text else ""
            
#             roistat_data = {
#                 'roistat': request.COOKIES.get('roistat_visit'),
#                 'key': 'ODNiNmJjODU1ZmY5Mzc5Nzg2M2I5NTliODdkNjBiYWI6MjI1NDcw', # Votre clé Roistat
#                 'sync': '0',
#                 'is_skip_sending': '0',
#                 'title': f'{title_prefix} №{order.id}',
#                 'comment': order_text,
#                 'name': request.POST.get("name"),
#                 'email': request.POST.get("email"),
#                 'phone': request.POST.get("phone"),
#                 'fields[UF_CRM_62CC22E9F3BED]': '{visit}',
#                 'fields[UF_CRM_1665139612]': '{landingPage}',
#                 'fields[UF_CRM_1665139637]': request.META.get('HTTP_HOST'),
#                 'fields[UF_CRM_1665139679]': '{source}',
#                 'fields[UF_CRM_1665139714]': '{city}',
#                 'fields[UTM_CAMPAIGN]': '{utmCampaign}',
#                 'fields[UTM_CONTENT]': '{utmContent}',
#                 'fields[UTM_MEDIUM]': '{utmMedium}',
#                 'fields[UTM_SOURCE]': '{utmSource}',
#                 'fields[UTM_TERM]': '{utmTerm}',
#                 'fields[STAGE_ID]': 'FINAL_INVOICE'
#             }
            
#             # Filtrer les valeurs None pour urlencode
#             roistat_data = {k: v for k, v in roistat_data.items() if v is not None}
            
#             data = urlencode(roistat_data).encode('utf-8')
#             url = 'https://cloud.roistat.com/api/proxy/1.0/leads/add'
#             req = Request(url, data=data)

#             with urlopen(req) as response:
#                 response_body = response.read().decode('utf-8')
#                 with open('roistat_response.log', 'a') as f:
#                     f.write(response_body + '\n')

#         except Exception as e:
#             with open("roistat_send_error.log", "a") as logf:
#                 logf.write(str(traceback.format_exc()) + '\n')

#     def post(self, request):
#             postdata = request.POST
#             response_data = {}

#             # 1. CAS : ACTIONS SUR LES ARTICLES DU PANIER (Update/Delete)
#             if 'submit' in postdata and postdata['submit'] in ['Update', ' ']:
#                 if postdata['submit'] == 'Update':
#                     cart.update_cart(request)
#                     return JsonResponse({'status': 'updated', 'item_id': postdata.get('item_id')})
#                 if postdata['submit'] == ' ':
#                     cart.remove_from_cart(request)
#                     return JsonResponse({'status': 'deleted', 'item_id': postdata.get('item_id')})

#             # 2. CAS : RAPPEL TÉLÉPHONIQUE (Modal callback)
#             # On vérifie si le champ 'text' contient la chaîne spécifique
#             elif postdata.get('text') == 'Заказ обратного звонка':
#                 form = CheckoutForm(postdata)
#                 if form.is_valid():
#                     order = form.save(commit=False)
#                     # if order.email == 'no-reply@pfkvet.ru':
#                     #     order.email = ''
#                     order.ip_address = request.META.get('REMOTE_ADDR')
#                     order.status = Order.SUBMITTED
#                     comment = form.cleaned_data.get('text_zayavka', '')
#                     order.text = f"Заказ обратного звонка. {comment}"
                    
#                     # Logique filiale
#                     current_filial = get_current_filial(request.get_host())
#                     order.address_to = current_filial.email
#                     order.save()

#                     self._send_to_roistat(request, order, title_prefix="Заказ звонка")
#                     checkout.task_send_mail_order(request, order)
                    
#                     # 1. Mettre le numéro de commande en session pour la page de reçu
#                     request.session['order_number'] = order.id
                    
#                     # 2. Renvoyer la réponse de succès AVEC l'URL de redirection
#                     return JsonResponse({
#                         'status': 'success', 
#                         'redirect_url': reverse('checkout:checkout_receipt')
#                     })
#                 else:
#                     return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

#             # 3. CAS : VALIDATION FINALE DU PANIER (Checkout)
#             elif postdata.get('submit_check') == 'checkout':
#                 order, errors = checkout.create_order(request)
#                 if order:
#                     request.session['order_number'] = order.id
#                     self._send_to_roistat(request, order, title_prefix="Заказ из корзины")
#                     return JsonResponse({'status': 'success', 'redirect_url': reverse('checkout:checkout_receipt')})
#                 else:
#                     return JsonResponse({'status': 'error', 'errors': errors.as_json()}, status=400)

#             # 4. CAS : DEMANDE DE PRIX (Modal price request)
#             elif postdata.get('submit_check_get_price') == 'checkout_get_price':
#                 form = CheckoutForm(postdata)
#                 if form.is_valid():
#                     order = form.save(commit=False)
#                     order.ip_address = request.META.get('REMOTE_ADDR')
                    
#                     order.status = Order.SUBMITTED
#                     product_slug = postdata.get('product_slug')
#                     try:
#                         product = Product.objects.get(slug=product_slug)
#                         order.text = f"Запрос цены на товар: {product.name_main} (slug: {product.slug})"
#                     except Product.DoesNotExist:
#                         order.text = f"Запрос цены на товар (slug: {product_slug} - не найден)"
#                     order.save()
                    
#                     self._send_to_roistat(request, order, title_prefix="Запрос цены")
#                     checkout.task_send_mail_order(request, order)
#                     request.session['order_number'] = order.id
#                     return JsonResponse({'status': 'success', 'redirect_url': reverse('checkout:checkout_receipt')})
#                 else:
#                     return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)


#             # 5. CAS : DEMANDE DE CONSULTATION (depuis la section "Callback Manager")
#             elif postdata.get('form_type') == 'consultation_request':
#                 form = CheckoutForm(postdata) # On utilise le même formulaire de validation
#                 if form.is_valid():
#                     order = form.save(commit=False)
                    
#                     # Le champ 'text' vient maintenant du formulaire
#                     order.text = form.cleaned_data.get('text', 'Запрос на консультацию')
                    
#                     # # Nettoyer l'email par défaut si vous l'avez
#                     # if order.email == 'no-reply@pkfcvet.ru':
#                     #     order.email = ''

#                     # Remplir les infos restantes
#                     order.ip_address = request.META.get('REMOTE_ADDR')
#                     order.status = Order.SUBMITTED
                    
#                     # Logique de la filiale
#                     current_filial = get_current_filial(request.get_host())
#                     order.address_to = current_filial.email
#                     # ... (logique gclid/yclid)
#                     order.save()

#                     self._send_to_roistat(request, order, title_prefix="Консультация со специалистом")
#                     checkout.task_send_mail_order(request, order)
                    
#                     # Réponse de succès SANS redirection
#                     request.session['order_number'] = order.id
#                     return JsonResponse({'status': 'success', 'redirect_url': reverse('checkout:checkout_receipt')})
#                 else:
#                     # Réponse d'erreur avec les détails de validation
#                     return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
    
#             # 6. CAS : AJOUT D'UN PRODUIT AU PANIER (Listing)
#             # On identifie ce cas par la présence de 'product_slug'
#             elif 'product_slug' in postdata:
#                 form = ProductAddToCartForm(data=postdata, request=request)
#                 if form.is_valid():
#                     cart.add_to_cart(request)
#                     if postdata.get('expres_oformit'):
#                         return JsonResponse({'status': 'added_and_redirect', 'redirect_url': reverse('cart:show_cart')})
#                     return JsonResponse({'status': 'added'})
#                 else:
#                     return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

#             # 6. CAS PAR DÉFAUT : ERREUR
#             return JsonResponse({'status': 'error', 'message': 'Неизвестный тип формы.'}, status=400)





# Dans menu/views_form.py

class SendFormOrder(View):
    """
    Classe refactorisée qui gère toutes les soumissions de formulaires AJAX.
    """

    # --- MÉTHODES D'AIDE PRIVÉES ---

    def _send_to_roistat(self, request, order, title_prefix=""):
        """
        Méthode privée pour envoyer les données à Roistat.
        Factorisée pour éviter la duplication de code.
        """
        try:
            order_text = order.text if order.text else ""
            
            roistat_data = {
                'roistat': request.COOKIES.get('roistat_visit'),
                'key': 'ODNiNmJjODU1ZmY5Mzc5Nzg2M2I5NTliODdkNjBiYWI6MjI1NDcw', # Votre clé Roistat
                'sync': '0',
                'is_skip_sending': '0',
                'title': f'{title_prefix} №{order.id}',
                'comment': order_text,
                'name': request.POST.get("name"),
                'email': request.POST.get("email"),
                'phone': request.POST.get("phone"),
                'fields[UF_CRM_62CC22E9F3BED]': '{visit}',
                'fields[UF_CRM_1665139612]': '{landingPage}',
                'fields[UF_CRM_1665139637]': request.META.get('HTTP_HOST'),
                'fields[UF_CRM_1665139679]': '{source}',
                'fields[UF_CRM_1665139714]': '{city}',
                'fields[UTM_CAMPAIGN]': '{utmCampaign}',
                'fields[UTM_CONTENT]': '{utmContent}',
                'fields[UTM_MEDIUM]': '{utmMedium}',
                'fields[UTM_SOURCE]': '{utmSource}',
                'fields[UTM_TERM]': '{utmTerm}',
                'fields[STAGE_ID]': 'FINAL_INVOICE'
            }
            
            # Filtrer les valeurs None pour urlencode
            roistat_data = {k: v for k, v in roistat_data.items() if v is not None}
            
            data = urlencode(roistat_data).encode('utf-8')
            url = 'https://cloud.roistat.com/api/proxy/1.0/leads/add'
            req = Request(url, data=data)

            with urlopen(req) as response:
                response_body = response.read().decode('utf-8')
                with open('roistat_response.log', 'a') as f:
                    f.write(response_body + '\n')

        except Exception as e:
            with open("roistat_send_error.log", "a") as logf:
                logf.write(str(traceback.format_exc()) + '\n')

    def _create_order_from_form(self, form, request, text_template, roistat_title):
        """
        Méthode universelle pour créer, sauvegarder et notifier une commande.
        Prend un formulaire Django valide et des paramètres de configuration.
        Retourne l'objet Order créé.
        """
        # 1. Créer l'objet Order à partir du formulaire, sans le sauvegarder
        order = form.save(commit=False)
        
        # 2. Remplir les champs communs qui ne viennent pas du formulaire
        order.ip_address = request.META.get('REMOTE_ADDR')
        order.status = Order.SUBMITTED
        order.user = request.user if request.user.is_authenticated else None

        # 3. Nettoyer les valeurs potentiellement "fausses"
        #    (Ex: si on a utilisé un email par défaut dans le HTML)
        # if order.email == 'no-reply@pkfcvet.ru':
        #     order.email = ''
            
        # 4. Construire le champ 'text' de la commande
        #    On utilise le template de texte fourni et on le formate avec les données disponibles.
        
        # Récupérer les données dont le template pourrait avoir besoin
        comment = form.cleaned_data.get('text_zayavka', '')
        product_slug = request.POST.get('product_slug')
        product_name = ''
        if product_slug:
            try:
                # On essaie de récupérer le nom du produit pour un message plus clair
                product = Product.objects.get(slug=product_slug)
                product_name = product.name_main
            except Product.DoesNotExist:
                product_name = f"(produit non trouvé: {product_slug})"

        # Remplacer les placeholders dans le template de texte
        order.text = text_template.format(
            comment=comment,
            product_slug=product_slug,
            product_name=product_name
        )
        
        # 5. Gérer la logique de la filiale et l'adresse de destination
        current_filial = get_current_filial(request.get_host())
        order.address_to = current_filial.email
        
        traffic_source = request.session.get(settings.CONTACTS_SESSION_KEY, '')
        if traffic_source == 'yclid' and current_filial.email_yclid:
            order.address_to = current_filial.email_yclid
        elif traffic_source == 'gclid' and current_filial.email_gclid:
            order.address_to = current_filial.email_gclid
        
        # 6. Sauvegarder l'objet Order complet en base de données
        order.save()

        # 7. Lancer les actions post-sauvegarde (notifications)
        self._send_to_roistat(request, order, title_prefix=roistat_title)
        # checkout.task_send_mail_order(request, order)
        
        # 8. Retourner l'objet créé pour que la méthode post puisse l'utiliser
        return order

    # --- MÉTHODE POST PRINCIPALE (LE "ROUTEUR") ---

    def post(self, request):
        postdata = request.POST

        # 1. Identifier l'action demandée
        action = None
        if 'submit' in postdata and postdata['submit'] == 'Update': action = 'update_cart'
        elif 'submit' in postdata and postdata['submit'] == ' ': action = 'delete_from_cart'
        elif postdata.get('submit_check') == 'checkout': action = 'checkout_cart'
        elif postdata.get('text') == 'Заказ обратного звонка': action = 'callback_request'
        elif postdata.get('submit_check_get_price') == 'checkout_get_price': action = 'price_request'
        elif postdata.get('form_type') == 'consultation_request': action = 'consultation_request'
        elif 'product_slug' in postdata and 'quantity' in postdata: action = 'add_to_cart'
        
        # 2. Exécuter l'action correspondante
        if action == 'update_cart':
            cart.update_cart(request)
            return JsonResponse({'status': 'updated', 'item_id': postdata.get('item_id')})
        
        elif action == 'delete_from_cart':
            cart.remove_from_cart(request)
            return JsonResponse({'status': 'deleted', 'item_id': postdata.get('item_id')})

        elif action == 'add_to_cart':
            form = ProductAddToCartForm(data=postdata, request=request)
            if form.is_valid():
                cart.add_to_cart(request)
                if postdata.get('expres_oformit'):
                    return JsonResponse({'status': 'added_and_redirect', 'redirect_url': reverse('cart:show_cart')})
                return JsonResponse({'status': 'added'})
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

        elif action == 'checkout_cart':
            order, errors = checkout.create_order(request) # create_order est déjà bien factorisé
            if order:
                request.session['order_number'] = order.id
                self._send_to_roistat(request, order, title_prefix="Заказ из корзины")
                return JsonResponse({'status': 'success', 'redirect_url': reverse('checkout:checkout_receipt')})
            return JsonResponse({'status': 'error', 'errors': errors.as_json()}, status=400)

        # Les actions suivantes utilisent toutes CheckoutForm et créent un Order
        elif action in ['callback_request', 'price_request', 'consultation_request']:
            form = CheckoutForm(postdata)
            if form.is_valid():
                # Définir les paramètres spécifiques à chaque formulaire
                if action == 'callback_request':
                    text_template = "Заказ обратного звонка. Комментарий: {comment}"
                    roistat_title = "Заказ звонка"
                elif action == 'price_request':
                    text_template = "Запрос цены на товар (slug: {product_slug})"
                    roistat_title = "Запрос цены"
                elif action == 'consultation_request':
                    text_template = form.cleaned_data.get('text', 'Запрос на консультацию')
                    roistat_title = "Консультация"
                
                # Appeler la méthode universelle de création de commande
                order = self._create_order_from_form(form, request, text_template, roistat_title)
                
                request.session['order_number'] = order.id
                return JsonResponse({'status': 'success', 'redirect_url': reverse('checkout:checkout_receipt')})
            
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

        # Si aucune action n'a été reconnue
        return JsonResponse({'status': 'error', 'message': 'Неизвестный тип формы.'}, status=400)