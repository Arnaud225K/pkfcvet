from django.db import models
from django.db.models.signals import post_delete, pre_save
from tinymce import models as tinymce_models
from transliterate import translit
import os


class Pricelists(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    date = models.DateTimeField(verbose_name='Дата последнего обновления')
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True, null=True, editable=False)
    name_title = models.CharField(max_length=1024, verbose_name="Название (заголовок)", editable=False)
    title_main = models.CharField(max_length=1024, verbose_name="Показывать заголовок группы", blank=True, null=True, editable=False)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True, editable=False)
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, editable=False)
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True,null=True, editable=False)
    file = models.FileField(upload_to='uploads/files', verbose_name="Файл прайс-листа")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Прайс-листы"
        
def delete_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if (text_block.file):
        if os.path.exists(text_block.file.path):
            os.remove(text_block.file.path)

def save_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if(text_block.id):
        obj =  Pricelists.objects.get(id=text_block.id)
        if (obj.file):
            if ( (not text_block.file) or obj.file.path !=  text_block.file.path):
                if os.path.exists(obj.file.path):
                    os.remove(obj.file.path)

post_delete.connect(delete_filefield, Pricelists)
pre_save.connect(save_filefield, Pricelists)


class PricelistsMain(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    date = models.DateTimeField(verbose_name='Дата последнего обновления')
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True, null=True, editable=False)
    name_title = models.CharField(max_length=1024, verbose_name="Название (заголовок)", editable=False)
    title_main = models.CharField(max_length=1024, verbose_name="Показывать заголовок группы", blank=True, null=True, editable=False)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True, editable=False)
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, editable=False)
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True,null=True, editable=False)
    file = models.FileField(upload_to='uploads/files', verbose_name="Файл прайс-листа")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Прайс-лист и опросник (общие)"
        db_table = 'pricelists_pricelistsmain'

def delete_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if (text_block.file):
        if os.path.exists(text_block.file.path):
            os.remove(text_block.file.path)

def save_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if(text_block.id):
        obj =  Pricelists.objects.get(id=text_block.id)
        if (obj.file):
            if ( (not text_block.file) or obj.file.path !=  text_block.file.path):
                if os.path.exists(obj.file.path):
                    os.remove(obj.file.path)

post_delete.connect(delete_filefield, PricelistsMain)
pre_save.connect(save_filefield, PricelistsMain)

