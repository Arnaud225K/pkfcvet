# -*- coding: utf-8 -*-
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.core import urlresolvers

# from django.http import HttpResponseRedirect
# from checkout.forms import CheckoutForm

# from checkout.models import Order, OrderItem
# from checkout import checkoutpy as checkout
# from cart import cartpy as cart

# # from accounts import profile


# def show_checkout(request, template_name='cart/cart.html'):
#     if cart.is_empty(request):
#         cart_url = urlresolvers.reverse('show_cart')
#         return HttpResponseRedirect(cart_url)
#     cart_items = cart.get_cart_items(request)
#     page_title = 'Shopping Cart'
#     cart_subtotal = cart.cart_subtotal(request)
#     mytemplate = template_name
#     return HttpResponseRedirect("/cart/")


# def receipt(request, template_name='checkout/receipt.html'):
#     order_number = request.session.get('order_number','')
#     if order_number:
#         order = Order.objects.filter(id=order_number)[0]
#         order_items = OrderItem.objects.filter(order=order)
#         del request.session['order_number']
#     else:
#         cart_url = urlresolvers.reverse('show_cart')
#         return HttpResponseRedirect(cart_url)
#     mytemplate = template_name
#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))




from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CheckoutForm
from .models import Order, OrderItem
from . import checkoutpy as checkout
from cart import cartpy as cart
from menu.views_form import get_current_filial



def show_checkout(request, template_name='cart/cart.html'):
    if cart.is_empty(request):
        return redirect('cart:show_cart')
    
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    mytemplate = template_name
    return redirect("/cart/") 


# def receipt(request, template_name='checkout/receipt.html'):
#     order_number = request.session.get('order_number', '')
    
#     if order_number:
#         try:
#             order = Order.objects.get(id=order_number)
#             order_items = OrderItem.objects.filter(order=order)
#             del request.session['order_number']
#         except Order.DoesNotExist:
#             return redirect('cart:show_cart')
#     else:
#         return redirect('cart:show_cart')

#     context = {
#         'order': order,
#         'order_items': order_items,
#         'request': request, 
#         'template_name': template_name,
#         'order_number': order_number,
#     }
#     return render(request, template_name, context)


def receipt(request, template_name='checkout/receipt.html'):
    order_number = request.session.get('order_number', '')
    
    if order_number:
        try:
            order = Order.objects.get(id=order_number)
            order_items = OrderItem.objects.filter(order=order)
            del request.session['order_number']
        except Order.DoesNotExist:
            return redirect('cart:show_cart')
    else:
        return redirect('cart:show_cart')

    current_filial = get_current_filial(request.get_host())

    context = {
        'order': order,
        'order_items': order_items,
        'order_number': order_number,
        'current_filial': current_filial,
    }
    return render(request, template_name, context)