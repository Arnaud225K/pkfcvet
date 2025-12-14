from django.db import models
from django.utils.translation import gettext_lazy as _ 


class StaticText(models.Model):
    slug = models.SlugField(max_length=1024, verbose_name="Латинское название [системное]")
    text = models.TextField(verbose_name="HTML текст", blank=True, null=True)
    template = models.FileField(upload_to='uploads/templates', verbose_name="Файл HTML шаблона", blank=True, null=True, default="", editable=False)
    comment = models.CharField(max_length=1024, verbose_name="Комментарий", blank=True, null=True, default="")

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Статические тексты"
