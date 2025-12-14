from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from tinymce import models as tinymce_models
from transliterate import translit
import os


class SpecPredlozhenie(models.Model):
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", blank=True, null=True)
    text = tinymce_models.HTMLField(verbose_name="Текст", blank=True, null=True)
    developer = models.CharField(max_length=1024, verbose_name="Производитель", blank=True, null=True)
    develop_in = models.CharField(max_length=1024, verbose_name="Страна производитель", blank=True, null=True)
    made_in = models.CharField(max_length=1024, verbose_name="Способ изготовления", blank=True, null=True)
    gost = models.CharField(max_length=1024, verbose_name="ГОСТ", blank=True, null=True)
    marka = models.CharField(max_length=1024, verbose_name="Марка", blank=True, null=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Новая Цена", blank=True, null=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Старая цена", blank=True, null=True)
    full_text = tinymce_models.HTMLField(verbose_name="Полный Текст", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    isShowMain = models.BooleanField(verbose_name="Отображать на главной", blank=True, db_column='isshowmain')
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('specpredl', kwargs={'specpredl_slug': self.name_lat})

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Спецпредложения"



@receiver(post_delete, sender=SpecPredlozhenie)
def delete_spec_image(sender, instance, **kwargs):
    """ Supprime le fichier image lorsque l'objet SpecPredlozhenie est supprimé. """
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=SpecPredlozhenie)
def update_spec_image_and_slug(sender, instance, **kwargs):
    """ Met à jour le slug et supprime l'ancienne image si elle change. """
    if not instance.name_lat and instance.name:
        slug_base = translit(instance.name, "ru", reversed=True)
        instance.name_lat = "".join(c if c.isalnum() or c in "-_" else "_" for c in slug_base).lower()

    if not instance.pk:
        return

    try:
        old_instance = SpecPredlozhenie.objects.get(pk=instance.pk)
    except SpecPredlozhenie.DoesNotExist:
        return

    if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)
