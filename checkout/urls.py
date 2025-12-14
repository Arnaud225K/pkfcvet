from django.urls import re_path
from . import views

app_name = 'checkout'

urlpatterns = [
    re_path(r'^$', views.show_checkout, {'template_name': 'checkout/checkout.html'}, name='checkout'),
    re_path(r'^receipt/$', views.receipt, {'template_name': 'checkout/receipt.html'}, name='checkout_receipt'),
]
