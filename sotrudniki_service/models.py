from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from menu.models import MenuCatalog
from tinymce import models as tinymce_models
import os



class SotrudnikiService(models.Model):
    position = models.ForeignKey(MenuCatalog, on_delete=models.CASCADE, verbose_name="Раздел меню")
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True, editable=False)
    name = models.CharField(max_length=1024, verbose_name="Имя")
    text = tinymce_models.HTMLField(verbose_name="Текст", blank=True, null=True, editable=False)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order_number"]
        verbose_name_plural = "Сотрудники-консультанты"



@receiver(post_delete, sender=SotrudnikiService)
def delete_sotrudnik_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=SotrudnikiService)
def update_sotrudnik_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = SotrudnikiService.objects.get(pk=instance.pk)
    except SotrudnikiService.DoesNotExist:
        return

    if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)

