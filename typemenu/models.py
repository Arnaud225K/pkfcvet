from django.db import models


class TypeMenu(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название типа")
    template = models.CharField(max_length=1024, verbose_name="Название файла шаблона")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Тип меню"
