from django.db import models


class TypeTextBlock(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    template = models.CharField(max_length=1024, verbose_name="Название файла шаблона")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Тип текстовых блоков"
        db_table = 'typetextblock_typetextblock'
