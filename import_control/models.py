from django.db import models
from tinymce import models as tinymce_models



class ImportControl(models.Model):
    slug = models.CharField(max_length=1024, verbose_name="Имя латинское")
    dublicate_id = models.CharField(max_length=256, verbose_name='id дубликата')
    original_id = models.CharField(max_length=256, verbose_name='id оригинала')
    date = models.DateTimeField(verbose_name='Дата', auto_now=True)
    info = models.TextField(verbose_name="Информация о продукте")
    result = models.TextField(verbose_name="Результат контроля")

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Контроль импортируемой продукции"
