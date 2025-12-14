# from django import forms
# from checkout.models import Order
# import datetime
# import re


# def strip_non_numbers(data):
#     """ gets rid of all non-number characters """
#     non_numbers = re.compile(r'\D')
#     return non_numbers.sub('', data)


# class CheckoutForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CheckoutForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['size'] = '30'

#     class Meta:
#         model = Order
#         exclude = ('status', 'ip_address', 'user', 'transaction_id', )


#     def clean_phone(self):
#         phone = self.cleaned_data['phone']
#         stripped_phone = strip_non_numbers(phone)
#         if len(stripped_phone) < 10:
#             raise forms.ValidationError(u'Введите корректный номер телефона (пример: 89121234567)')
#         return self.cleaned_data['phone']



from django import forms
from .models import Order
import re

def strip_non_numbers(data):
    non_numbers = re.compile(r'\D')
    return non_numbers.sub('', data)

class CheckoutForm(forms.ModelForm):
    # --- AJOUT DES CHAMPS MANQUANTS ---
    consent = forms.BooleanField(
        required=False, # Ce champ est optionnel
        label="Я принимаю условия политики конфиденциальности"
    )
    consent_2 = forms.BooleanField(
        required=True, # Ce champ est obligatoire
        label="Я выражаю согласие на обработку персональных данных",
        error_messages={'required': 'Необходимо выразить согласие на обработку персональных данных.'}
    )
    
    # Champ caché pour le type de formulaire
    # text = forms.CharField(max_length=255, widget=forms.HiddenInput())
    text = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    # Champ optionnel pour le commentaire
    text_zayavka = forms.CharField(widget=forms.Textarea, required=False)

    form_type = forms.CharField(required=False, widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        # Vous pouvez supprimer cette boucle si vous n'en avez plus besoin
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'

    class Meta:
        model = Order
        # On ne veut pas que le formulaire gère 'text', on le fera manuellement
        fields = ['name', 'phone', 'email']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Si le formulaire est pour la newsletter, le téléphone n'est pas requis
        # 'self.data' permet d'accéder aux données POST brutes
        if self.data.get('text') == 'Заказ рассылки':
            return phone
            
        if not phone:
             raise forms.ValidationError('Требуется номер телефона.')

        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Введите корректный номер телефона (пример: 89121234567).')
        return phone
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Si le formulaire est pour la newsletter, l'email est requis
        if self.data.get('text') == 'Заказ рассылки' and not email:
            raise forms.ValidationError('Требуется адрес электронной почты для подписки.')
        return email