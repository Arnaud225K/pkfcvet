from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from menu.models import MenuCatalog
from TypeTextBlock.models import TypeTextBlock
from tinymce import models as tinymce_models

import os


class TextBlockMenu(models.Model):
    position = models.ForeignKey(MenuCatalog, on_delete=models.CASCADE, verbose_name="Раздел меню")
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    type = models.ForeignKey(TypeTextBlock, on_delete=models.SET_NULL, verbose_name="Тип текстового блока", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    date = models.DateTimeField(verbose_name='Дата', blank=True, null=True)
    text = tinymce_models.HTMLField(verbose_name="Текст", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')
    video = models.CharField(max_length=4096, verbose_name="Видео на Youtube", blank=True, null=True)
    isHiddenVideo = models.BooleanField(verbose_name="Не показывать видео", blank=True, db_column='ishiddenvideo')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Текстовый блок (меню)"
        db_table = "textblockmenu_textblockmenu"



@receiver(post_delete, sender=TextBlockMenu)
def delete_textblockmenu_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=TextBlockMenu)
def update_textblockmenu_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = TextBlockMenu.objects.get(pk=instance.pk)
    except TextBlockMenu.DoesNotExist:
        return

    if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)
