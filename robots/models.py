from django.db import models
from Filials.models import Filials



class RobotsTxt(models.Model):
    filial = models.ForeignKey(Filials, on_delete=models.CASCADE, verbose_name="Родительский пункт")
    text = models.TextField(verbose_name="Содержимое robots.txt")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        return self.filial.name

    class Meta:
        verbose_name_plural = u"Содержимое robots.txt (в зависимости от региона)"