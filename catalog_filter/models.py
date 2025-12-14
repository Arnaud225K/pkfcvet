from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from transliterate import translit
import re 
from menu.models import MenuCatalog


class CatalogFilterName(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    is_hidden = models.BooleanField(verbose_name="Скрыть", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Фильтры"


class CatalogFilterValue(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    
    category = models.ForeignKey(MenuCatalog, on_delete=models.CASCADE, verbose_name="Название категории")
    filter_name = models.ForeignKey(CatalogFilterName, on_delete=models.CASCADE, verbose_name="Название фильтра")
    
    value = models.CharField(max_length=1024, verbose_name="Значение параметра")
    value_lat = models.CharField(max_length=1024, verbose_name="Значение параметра латинское", blank=True)
    is_hidden = models.BooleanField(verbose_name="Скрыть", blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.filter_name.name}: {self.value}"

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Значения фильтров"



@receiver(pre_save, sender=CatalogFilterName)
def generate_filter_name_slug(sender, instance, **kwargs):
    """ Génère un slug pour le nom du filtre avant de sauvegarder. """
    if not instance.name_lat and instance.name:
        slug_base = translit(instance.name, "ru", reversed=True)
        instance.name_lat = "".join(c if c.isalnum() or c in "-_" else "_" for c in slug_base).lower()


# @receiver(pre_save, sender=CatalogFilterValue)
# def generate_filter_value_slug(sender, instance, **kwargs):
#     """ Génère un slug pour la valeur du filtre avant de sauvegarder. """
#     if not instance.value_lat and instance.value:
#         slug_base = translit(instance.value, "ru", reversed=True)
#         instance.value_lat = "".join(c if c.isalnum() or c in "-_" else "_" for c in slug_base).lower()

def generate_filter_value_slug(sender, instance, **kwargs):
    """ Génère un slug pour la valeur du filtre avant de sauvegarder. """
    if not instance.value_lat and instance.value:
        value_for_slug = str(instance.value).replace(',', '.')
        slug_base = translit(value_for_slug, "ru", reversed=True)
        slug = re.sub(r'[^\w-]', '', slug_base.replace('.', '-')).lower()
        instance.value_lat = slug