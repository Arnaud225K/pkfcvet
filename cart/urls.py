from django.urls import re_path
from . import views

app_name = 'cart'

urlpatterns = [
    re_path(r'^$', views.show_cart, {'template_name': 'cart/cart.html'}, name='show_cart'),
]