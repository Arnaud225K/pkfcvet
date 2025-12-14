from django.db import models
from django import forms
from django.contrib.auth.models import User
# from menu.models import Product
import decimal
from django.conf import settings
from django.db import models
from django.urls import reverse 


class BaseOrderInfo(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(verbose_name="Ф.И.О",max_length=50)
    email = models.EmailField(verbose_name="E-mail",max_length=50)
    phone = models.CharField(verbose_name="Телефон",max_length=20)


class Order(BaseOrderInfo):
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                    (PROCESSED, 'Processed'),
                    (SHIPPED, 'Shipped'),
                    (CANCELLED, 'Cancelled'),)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(verbose_name="Статус", choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=20)
    text = models.TextField(verbose_name="Текст", blank=True, null=True)
    card_organization = models.FileField(upload_to='uploads/files', verbose_name="Карточка предприятия", blank=True, null=True)
    address_to = models.CharField(max_length=256, verbose_name="Отправлен", blank=True, null=True)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ #{self.id}'

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    def get_absolute_url(self):
        return reverse('order_details', kwargs={'order_id': self.id})



class OrderItem(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product = models.ForeignKey('menu.Product', on_delete=models.PROTECT)

    quantity = models.DecimalField(max_digits=9, decimal_places=2, default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name_main or 'Produit inconnu'} (Commande #{self.order.id})"

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name_main or ''


    def get_absolute_url(self):
        return self.product.get_absolute_url()


