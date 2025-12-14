from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver 
from django.utils.translation import gettext_lazy as _ 

import os


class Slider(models.Model):
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=256, verbose_name="Название")
    text = models.CharField(max_length=256, verbose_name="Текст", blank=True, null=True)
    text_more = models.CharField(max_length=256, verbose_name="Текст дополнительно", blank=True, null=True)
    string_down = models.CharField(max_length=256, verbose_name="Текст дополнительный", blank=True, null=True, editable=False)
    url = models.CharField(max_length=256, verbose_name="Ссылка", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Слайдер"


@receiver(post_delete, sender=Slider)
def delete_slider_image(sender, instance, **kwargs):
    """ Supprime le fichier image lorsque l'objet Slider est supprimé. """
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Slider)
def update_slider_image(sender, instance, **kwargs):
    """ Supprime l'ancienne image si elle est modifiée ou effacée. """
    if not instance.pk:
        return

    try:
        old_instance = Slider.objects.get(pk=instance.pk)
    except Slider.DoesNotExist:
        return 

    if not old_instance.image:
        return

    new_image_exists = bool(instance.image)
    if not new_image_exists or old_instance.image.path != instance.image.path:
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)
