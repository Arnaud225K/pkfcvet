from django.conf import settings
from django.db import models
from menu.models import Product


class PageView(models.Model):
    class Meta:
        abstract = True

    date = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_id = models.CharField(max_length=50, default='')


class ProductView(PageView):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        product_name = self.product.name_main if self.product else "Produit supprimé"
        user_info = f" par {self.user}" if self.user else " par un visiteur anonyme"
        return f"Vue du produit '{product_name}'{user_info} le {self.date.strftime('%Y-%m-%d %H:%M')}"