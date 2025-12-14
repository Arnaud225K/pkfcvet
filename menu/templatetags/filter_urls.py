from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def build_filter_url(context, filter_type, filter_value):
    """
    Construit une URL de filtre dynamique.
    Ex: {% build_filter_url 'gost' item.gost__number_lat %}
    """
    current_menu = context.get('current_menu')
    if not current_menu:
        return '#'

    applied_filters = {
        'marka': context.get('marka_lat'),
        'gost': context.get('gost_lat'),
        's1': context.get('s1_lat'),
        's2': context.get('s2_lat'),
        's3': context.get('s3_lat'),
        's4': context.get('s4_lat'),
        's5': context.get('s5_lat'),
        's6': context.get('s6_lat'),
        's7': context.get('s7_lat'),
    }

    applied_filters[filter_type] = filter_value

    filter_parts = []
    for key, value in applied_filters.items():
        if value:
            filter_parts.append(f"{key}={value}")

    if not filter_parts:
        return current_menu.get_absolute_url()

    filters_str = "/".join(filter_parts)
    
    return reverse('menu:menu_catalog_filtered', kwargs={
        'menu_slug': current_menu.slug,
        'filters_str': filters_str
    })