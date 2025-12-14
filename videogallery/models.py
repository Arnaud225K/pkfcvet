# -*- coding: utf-8 -*-
from django.db import models
from tinymce import models as tinymce_models


# Create your models here.
class Videogallery(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    url = models.CharField(max_length=1024, verbose_name="url (youtube) ТОЛЬКО НОМЕР")
    date = models.DateTimeField(verbose_name=u'Дата')
    title_main = models.CharField(max_length=1024, verbose_name="Показывать заголовок группы", blank=True, null=True, editable=False)
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True,null=True, editable=False)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Видеогаллерея"



