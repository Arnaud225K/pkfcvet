# -*- coding: utf-8 -*-
from django.db import models

import os

from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save
from transliterate import translit
from django.urls import reverse


class Metall(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    isCvetMet = models.BooleanField(verbose_name="Цветной металл?", blank=True, db_column='iscvetmet')
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Металл (верхний уровень)"

    def get_list_metall_group(self):
        return MetallGroup.objects.filter(position=self.id, isHidden=False)

    def get_absolute_url(self):
        return reverse('metall_group', kwargs={'metall_group_slug': self.name_lat})


class MetallGroup(models.Model):
    position = models.ForeignKey(Metall, on_delete=models.CASCADE, verbose_name="Металл")
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Разновидности металла (средний уровень)"

    def get_list_marka_metall(self):
        return MarkaMetall.objects.filter(position=self.id, isHidden=False)

    def get_absolute_url(self):
        return reverse('metall_group', kwargs={'metall_group_slug': self.name_lat})


class MarkaMetall(models.Model):
    position = models.ForeignKey(MetallGroup, on_delete=models.CASCADE, verbose_name="Разновидность металла")
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')
    hiddenSite = models.BooleanField(verbose_name="Скрыть из листингов", blank=True, default=False, db_column='hiddensite')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Марка металла (нижний уровень)"
        db_table = 'marochnik_markametall'

    def get_absolute_url(self):
        return reverse('marka_metall', kwargs={'marka_metall_slug': self.name_lat})


def save_filefield(sender, **kwargs):
    # from GOST.models import GOST
    # markaList = GOST.objects.all()
    # for item in markaList:
    #     item.save()
    categoryMetall = kwargs.get('instance')
    if categoryMetall.name_lat == "" or not categoryMetall.name_lat:
        categoryMetall.name_lat = slugify(translit(categoryMetall.name, "ru", reversed=True))
        # .replace(" ", "_").replace("*", "-").replace(";", "-").replace("\"", "-").replace("%", "-").replace(":", "-").replace(",", "").replace("'","").replace("(", "").replace(")", "").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_")
        # .replace(" ", "_").replace(",", "").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
        while MarkaMetall.objects.filter(name_lat=categoryMetall.name_lat):
            categoryMetall.name_lat = categoryMetall.name_lat + "_"

pre_save.connect(save_filefield, Metall)
pre_save.connect(save_filefield, MetallGroup)
pre_save.connect(save_filefield, MarkaMetall)