from django.db import models

from django.db.models.signals import pre_save
from transliterate import translit
from django.urls import reverse



class GOSTHead(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    number = models.CharField(max_length=1024, verbose_name="Обозначение")
    name = models.CharField(max_length=1024, verbose_name="Название")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "ГОСТ Область (верхний уровень)"
        db_table = 'gost_gosthead'


class GOSTGroup(models.Model):
    position = models.ForeignKey(GOSTHead, on_delete=models.CASCADE, verbose_name="ГОСТ Область")
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    number = models.CharField(max_length=1024, verbose_name="Обозначение")
    name = models.CharField(max_length=1024, verbose_name="Название")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.number + self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "ГОСТ Группа (средний уровень)"
        db_table = 'gost_gostgroup'


class GOST(models.Model):
    position = models.ForeignKey(GOSTGroup, on_delete=models.CASCADE, verbose_name="ГОСТ Группа")
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    number = models.CharField(max_length=1024, verbose_name="Обозначение")
    name = models.CharField(max_length=1024, verbose_name="Название")
    number_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.number

    class Meta:
        ordering = ["number"]
        verbose_name_plural = "ГОСТ (нижний уровень)"
        db_table = 'gost_gost'

    def get_absolute_url(self):
        return reverse('gost', kwargs={'gost_slug': self.number_lat})


def save_filefield(sender, **kwargs):
    from Marochnik.models import MarkaMetall, Metall, MetallGroup
    from menu.models import MenuCatalog

    markaList = MarkaMetall.objects.filter(name_lat="")
    for item in markaList:
        item.save()
    markaList = MarkaMetall.objects.filter(name_lat=None)
    for item in markaList:
        item.save()
    categoryMetall = kwargs.get('instance')
    if categoryMetall.number_lat == "":
        categoryMetall.number_lat = translit(categoryMetall.number.strip(), "ru", reversed=True).replace(" ", "_").replace(",", "").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()

pre_save.connect(save_filefield, GOST)