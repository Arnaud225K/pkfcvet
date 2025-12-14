

import json
import threading
import os
from transliterate import translit
from datetime import datetime

from django.core import serializers
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import default_storage

from cart import cartpy as cart
from checkout.forms import CheckoutForm
from menu.views_form import get_current_filial
from checkout.models import Order 


def get_today():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def send_mail_order(request_host, order_json, file_name=None, product=None):
    """
    Envoie l'email de notification de commande à l'adresse définie dans settings.py.
    """
    try:
        order_data = json.loads(order_json)[0]['fields']
        
        # 1. Construire l'email pour l'administrateur
        subject_admin = f"Поступил новый заказ: {order_data.get('name', 'Без имени')} от {order_data.get('date')}"
        
        body_admin = f"""Заказ от: {order_data.get('date')}

                    Ф.И.О: {order_data.get('name', 'Не указано')}
                    Телефон: {order_data.get('phone', 'Не указан')}
                    Адрес электронной почты: {order_data.get('email', 'Не указан')}

                    Текст заявки/комментарий:
                    ---------------------------
                    {order_data.get('text', 'Нет комментария')}
                    ---------------------------
                """
        
        # On utilise l'adresse email définie dans les settings
        admin_email_address = settings.ORDER_NOTIFICATION_EMAIL
        
        # S'assurer que la variable est bien définie
        if not admin_email_address:
            return

        email_admin = EmailMessage(
            subject_admin,
            body_admin,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email_address] if isinstance(admin_email_address, str) else admin_email_address
        )

        # 2. Ajouter le fichier joint si il existe
        if file_name:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                if os.path.exists(file_path):
                    email_admin.attach_file(file_path)
                else:
                    # print(f"Fichier joint non trouvé : {file_path}")
                    pass
            except Exception as e:
                pass
                # print(f"Erreur lors de l'attachement du fichier : {e}")

        # 3. Envoyer l'email
        email_admin.send(fail_silently=False)

        # print(f"Email de commande envoyé avec succès à {admin_email_address}")

    except Exception as e:
        # print(f"ERREUR CRITIQUE DANS LE THREAD D'ENVOI D'EMAIL: {e}")
        # import traceback
        # print(traceback.format_exc())
        pass


def task_send_mail_order(request, order, file_name=None, product=None):
    """Lance l'envoi d'email dans un thread."""
    try:
        # On passe le host et le JSON sérialisé au thread
        t = threading.Thread(
            target=send_mail_order,
            args=[request.get_host(), serializers.serialize('json', [order]), file_name, product]
        )
        t.setDaemon(True)
        t.start()
    except Exception as e:
        pass
        # print(f"Erreur lors du lancement du thread d'email: {e}")

def create_order(request):
    """
    Fonction principale pour créer une commande à partir du panier.
    Modernisée pour Python 3 et les formulaires Django.
    """
    # On utilise le même formulaire que pour les autres vues
    form = CheckoutForm(request.POST, request.FILES)

    if not form.is_valid():
        return (None, form.errors)

    order = form.save(commit=False)
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = request.user if request.user.is_authenticated else None
    order.status = Order.SUBMITTED 

    # Construire le champ 'text'
    cart_items = cart.get_cart_items(request)
    text_order = form.cleaned_data.get('text_zayavka', '') + "\n\nТовары в заказе:\n"
    for ci in cart_items:
        text_order += f"- {ci.product.name_main} (Кол-во: {ci.quantity})\n"
    order.text = text_order

    # Gérer le fichier uploadé
    file_path = None
    if 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        main_name = translit(uploaded_file.name.strip(), "ru", reversed=True)
        file_name_str = f'uploads/files/card_{get_today()}_{main_name}'
        file_path = default_storage.save(file_name_str, uploaded_file)
        order.card_organization = file_path

    # Gérer la filiale
    current_filial = get_current_filial(request.get_host())
    order.address_to = current_filial.email
    contact_type = request.session.get(settings.CONTACTS_SESSION_KEY, '')
    if contact_type == 'yclid' and current_filial.email_yclid:
        order.address_to = current_filial.email_yclid
    elif contact_type == 'gclid' and current_filial.email_gclid:
        order.address_to = current_filial.email_gclid
    
    order.save()
    
    # task_send_mail_order(request, order, file_name=file_path)
    
    cart.empty_cart(request)
    
    return (order, None)