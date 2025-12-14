from transliterate import translit
from django import template
# from django.contrib.flatpages.models import FlatPage
from cart import cartpy as cart
from menu.models import MenuCatalog
from pkfcvet import settings
register = template.Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items_quick = cart.get_cart_items(request)[:3]
    cart_subtotal = cart.cart_subtotal(request)
    return {'cart_item_count': cart_item_count,
            'cart_items_quick': cart_items_quick,
            'MEDIA_URL': settings.MEDIA_URL,
            'cart_subtotal': cart_subtotal}


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = MenuCatalog.objects.filter(is_active=True)
    return {
        'active_categories': active_categories,
        'request_path': request_path
    }


# @register.inclusion_tag("tags/footer.html")
# def footer_links():
#     flatpage_list = FlatPage.objects.all()
#     return {'flatpage_list': flatpage_list }


@register.inclusion_tag("tags/product_list.html")
def product_list(products, header_text):
    return {'products': products,
            'header_text': header_text}


def my_floatformat(value):
    try:
        value.replace(".", ",")
        value = float(value)
    except:
        pass
    try:
        value = int(value * 10000) / 10000.
        if str(value)[-2:] == ".0":
            value = str(value)[:-2]
    except:
        pass
    return value


register.filter('my_floatformat', my_floatformat)


def my_slugify(value):
    value = translit(value, "ru", reversed=True).replace(" ", "_").replace("+", "_").replace("\\", "_").replace(
        "\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace(
        "!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
    return value


register.filter('my_slugify', my_slugify)
