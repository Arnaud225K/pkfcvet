from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from tinymce import models as tinymce_models
from transliterate import translit
import os


class PhotogalleryGroup(models.Model):
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Группы фотографий"


class Photogallery(models.Model):
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    group = models.ForeignKey(PhotogalleryGroup, on_delete=models.CASCADE, verbose_name="Группа")
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True, null=True, editable=False)
    name_title = models.CharField(max_length=1024, verbose_name="Название (заголовок)", editable=False)
    title_main = models.CharField(max_length=1024, verbose_name="Показывать заголовок группы", blank=True, null=True)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True, editable=False)
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, editable=False)
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True, null=True, editable=False)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Фотогаллерея"



@receiver(post_delete, sender=Photogallery)
def delete_photogallery_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Photogallery)
def update_photogallery_image_and_slug(sender, instance, **kwargs):
    if not instance.name_lat and instance.name_title:
        slug_base = translit(instance.name_title, "ru", reversed=True)
        instance.name_lat = "".join(c if c.isalnum() or c in "-_" else "_" for c in slug_base).lower()

    if not instance.pk:
        return

    try:
        old_instance = Photogallery.objects.get(pk=instance.pk)
    except Photogallery.DoesNotExist:
        return

    if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)


