# -*- coding: utf-8 -*-
# this stuff goes at the top of the file, below other imports
# from django.core import urlresolvers

from django.http import HttpResponseRedirect
from cart import cartpy as cart

from django.shortcuts import get_object_or_404, render
# from menu.models import MenuCatalog, Product
from django.template import RequestContext
import pkfcvet.settings as settings
from checkout import checkoutpy as checkout


def show_cart(request, template_name="cart/cart.html"):
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render(request, template_name, locals())