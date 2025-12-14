# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete, pre_save
from tinymce import models as tinymce_models
import os


class Vacancy(models.Model):
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    text = tinymce_models.HTMLField(verbose_name="Текст")
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True, editable=False)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Вакансии"


def delete_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if (text_block.image):
        if os.path.exists(text_block.image.path):
            os.remove(text_block.image.path)


def save_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if(text_block.id):
        obj =  Vacancy.objects.get(id=text_block.id)
        if (obj.image):
            if ( (not text_block.image) or obj.image.path !=  text_block.image.path):
                if os.path.exists(obj.image.path):
                    os.remove(obj.image.path)

post_delete.connect(delete_filefield, Vacancy)
pre_save.connect(save_filefield, Vacancy)