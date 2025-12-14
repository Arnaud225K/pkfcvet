# -*- coding: utf-8 -*-
import os
from django.template import Context, Template

# from kzmc_kz import settings
from .models import StaticText
from pkfcvet.views import global_views


def static_text(request):
    static_text = {}
    for item in list(StaticText.objects.values('slug', 'text').order_by('slug')):
        static_text[item['slug']] = item

    


    try:
        checkout_cart = static_text['checkout_cart']['text']
    except:
        checkout_cart = ""
    try:
        button_email = static_text['button_email']['text']
    except:
        button_email = ""
    try:
        form_uznat_zcenu = static_text['form_uznat_zcenu']['text']
    except:
        form_uznat_zcenu = ""

    try:
        button_zayavka_kategoriya = static_text['button_zayavka_kategoriya']['text']
    except:
        button_zayavka_kategoriya = ""
    try:
        page404error = static_text['page404error']['text']
    except:
        page404error = ""
    try:
        button_opros_product = static_text['button_opros_product']['text']
    except:
        button_opros_product = ""
    try:
        button_email_product = static_text['button_email_product']['text']
    except:
        button_email_product = ""
    try:
        button_opros_emkosti = static_text['button_opros_emkosti']['text']
    except:
        button_opros_emkosti = ""
    try:
        button_opros_list_emkosti = static_text['button_opros_list_emkosti']['text']
    except:
        button_opros_list_emkosti = ""
    try:
        button_email_emkosti = static_text['button_email_emkosti']['text']
    except:
        button_email_emkosti = ""
    try:
        button_opros_list_detali = static_text['button_opros_list_detali']['text']
    except:
        button_opros_list_detali = ""
    try:
        button_email_detali = static_text['button_email_detali']['text']
    except:
        button_email_detali = ""
    try:
        form_podpiska_novosti = static_text['form_podpiska_novosti']['text']
    except:
        form_podpiska_novosti = ""
    try:
        button_podpiska_email = static_text['button_podpiska_email']['text']
    except:
        button_podpiska_email = ""
    try:
        email_contact = static_text['email_contact']['text']
    except:
        email_contact = ""
    try:
        card_company = static_text['card_company']['text']
    except:
        card_company = ""
    try:
        card_inn = static_text['card_inn']['text']
    except:
        card_inn = ""
    try:
        button_usluga = static_text['button_usluga']['text']
    except:
        button_usluga = ""
    try:
        button_email_opros = static_text['button_email_opros']['text']
    except:
        button_email_opros = ""
    try:
        button_opros_list = static_text['button_opros_list']['text']
    except:
        button_opros_list = ""
    try:
        perezvonite_mne_manager = static_text['perezvonite_mne_manager']['text']
    except:
        perezvonite_mne_manager = ""
    try:
        perezvonite_mne_today = static_text['perezvonite_mne_today']['text']
    except:
        perezvonite_mne_today = ""

    try:
        button_email_footer = static_text['button_email_footer']['text']
    except:
        button_email_footer = ""

    try:
        phone_besplatno_footer = static_text['phone_besplatno_footer']['text']
    except:
        phone_besplatno_footer = ""
    try:
        phone_filial_footer = static_text['phone_filial_footer']['text']
    except:
        phone_filial_footer = ""
    try:
        button_search = static_text['button_search']['text']
    except:
        button_search = ""
    try:
        phone_besplatno = static_text['phone_besplatno']['text']
    except:
        phone_besplatno = ""
    try:
        button_obratnii_zvonok = static_text['button_obratnii_zvonok']['text']
    except:
        button_obratnii_zvonok = ""
    try:
        phone_filial = static_text['phone_filial']['text']
    except:
        phone_filial = ""
    try:
        button_oformit_zayavky = static_text['button_oformit_zayavky']['text']
    except:
        button_oformit_zayavky = ""
    try:
        button_price = static_text['button_price']['text']
    except:
        button_price = ""
    try:
        button_perezvonite_mne = static_text['button_perezvonite_mne']['text']
    except:
        button_perezvonite_mne = ""
    try:
        copy_email = static_text['copy_email']['text']
    except:
        copy_email = ""
    try:
        button_zaprosit_ceny = static_text['button_zaprosit_ceny']['text']
    except:
        button_zaprosit_ceny = ""
    try:
        button_vernutsya = static_text['button_vernutsya']['text']
    except:
        button_vernutsya = ""
    try:
        block_price_mail_copy = static_text['block_price_mail_copy']['text']
    except:
        block_price_mail_copy = ""
    try:
        counter_popup_show = static_text['counter_popup_show']['text']
    except:
        counter_popup_show = ""
    try:
        counter_popup_not = static_text['counter_popup_not']['text']
    except:
        counter_popup_not = ""

    return locals()


# def get_static_text(global_context, slug):
#     html_static_text = ''

#     try:
#         html_static_text = Template(StaticText.objects.filter(slug=slug).first().text).render(Context(global_context))
#     except:
#         html_static_text = ''

#     return html_static_text
