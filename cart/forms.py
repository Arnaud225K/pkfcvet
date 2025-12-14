from django import forms
from cart.models import CartItem


# class ProductAddToCartForm(forms.Form):
#     quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2',
#                                 'value': '1', 'class': 'quantity', 'maxlength': '5'}),
#                                 error_messages={'invalid': 'Please enter a valid quantity.'}, min_value=1)
#     product_slug = forms.CharField(widget=forms.HiddenInput())

#     class Meta:
#         model = CartItem
#         fields = ('quantity',)

#     # override the default __init__ so we can set the request
#     def __init__(self, request=None, *args, **kwargs):
#         self.request = request
#         super(ProductAddToCartForm, self).__init__(*args, **kwargs)

#     # custom validation to check for cookies
#     def clean(self):
#         if self.request:
#             if not self.request.session.test_cookie_worked():
#                 raise forms.ValidationError("Cookies must be enabled.")
#         return self.cleaned_data




class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'size': '2', 'class': 'quantity', 'maxlength': '5'}),
        error_messages={'invalid': 'Пожалуйста, введите корректное количество.'},
        min_value=1,
        initial=1
    )
    product_slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ProductAddToCartForm, self).clean()
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError("Для добавления товаров в корзину необходимо включить cookies.")
        return cleaned_data