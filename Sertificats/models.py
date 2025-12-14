from django.db import models
from django.db.models.signals import post_delete, pre_save
from tinymce import models as tinymce_models
from transliterate import translit
import os


class SertificatsGroup(models.Model):
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Группы сертификатов"



class Sertificats(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    group = models.ForeignKey(SertificatsGroup, on_delete=models.CASCADE, verbose_name="Группа")
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True, null=True, editable=False)
    name_title = models.CharField(max_length=1024, verbose_name="Название (заголовок)", editable=False)
    title_main = models.CharField(max_length=1024, verbose_name="Показывать заголовок группы", blank=True, null=True)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True, editable=False)
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, editable=False)
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True,null=True, editable=False)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = u"Сертификаты"
        db_table = 'sertificats_sertificats'
        
def delete_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if (text_block.image):
        if os.path.exists(text_block.image.path):
            os.remove(text_block.image.path)

def save_filefield(sender, **kwargs):
    text_block = kwargs.get('instance')
    if text_block.name_lat == "":
        text_block.name_lat = translit(text_block.name_title, "ru", reversed=True).replace(" ", "_").replace(",", "").replace("+", "_").replace("\\", "_").replace("\"", "_").replace(")", "_").replace("(", "_").replace(".", "_").replace("'", "").replace(":", "_").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
    if(text_block.id):
        obj =  Sertificats.objects.get(id=text_block.id)
        if (obj.image):
            if ( (not text_block.image) or obj.image.path !=  text_block.image.path):
                if os.path.exists(obj.image.path):
                    os.remove(obj.image.path)

post_delete.connect(delete_filefield, Sertificats)
pre_save.connect(save_filefield, Sertificats)


