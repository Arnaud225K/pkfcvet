from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from tinymce import models as tinymce_models
from Filials.models import Filials
import os




class TextBlockUrl(models.Model):
    url = models.CharField(max_length=1024, verbose_name="url страницы")
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    date = models.DateTimeField(verbose_name='Дата', blank=True, null=True)
    filial = models.ForeignKey(Filials, on_delete=models.SET_NULL, verbose_name="Регион показа", blank=True, null=True)
    text = tinymce_models.HTMLField(verbose_name="Текст", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    title_main = models.CharField(max_length=1024, verbose_name="Заголовок страницы", blank=True, null=True)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True, help_text='Ключевые слова для SEO продвижения (через запятую). Мета тэг - keywords')
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, help_text='Содержимое мета тэга - description')
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Текстовый блок (ссылка)"
        db_table = 'textblockurl_textblockurl'



@receiver(post_delete, sender=TextBlockUrl)
def delete_textblock_image(sender, instance, **kwargs):
    """ Supprime le fichier image lorsque l'objet TextBlockUrl est supprimé. """
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=TextBlockUrl)
def update_textblock_image(sender, instance, **kwargs):
    """ Supprime l'ancienne image si elle est modifiée ou effacée. """
    if not instance.pk:
        return

    try:
        old_instance = TextBlockUrl.objects.get(pk=instance.pk)
    except TextBlockUrl.DoesNotExist:
        return

    if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)