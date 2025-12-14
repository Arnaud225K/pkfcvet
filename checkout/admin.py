from django.contrib import admin
from checkout.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'name', 'phone', 'email', 'address_to', 'text')
    list_filter = ('status', 'date')
    search_fields = ('email', 'name', 'text', 'id')
    # inlines = [OrderItemInline, ]
    fieldsets = (
        ('Info', {'fields': ('status', 'name', 'email', 'phone', 'text', 'ip_address', 'card_organization')}),
    )


admin.site.register(Order, OrderAdmin)
