from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models


class Contacts(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    text = tinymce_models.HTMLField(verbose_name="Текст", blank=True, null=True, editable=False)
    phone = models.CharField(max_length=1024, verbose_name="Телефон", blank=True, null=True, editable=False)
    phone_dop = models.CharField(max_length=1024, verbose_name="Телефон (дополнительный)", blank=True, null=True, editable=False)
    fax = models.CharField(max_length=1024, verbose_name="Факс", blank=True, null=True, editable=False)
    address = models.CharField(max_length=1024, verbose_name="Адрес", blank=True, null=True, editable=False)
    email = models.CharField(max_length=256, verbose_name="Электронная почта", blank=True, null=True, editable=False)
    rezhim = models.CharField(max_length=256, verbose_name="Режим работы", blank=True, null=True, editable=False)
    comment = models.CharField(max_length=256, verbose_name="Заголовок контактов", editable=False)
    text_head = models.TextField(verbose_name="Блок в head (внизу)", blank=True, null=True)
    text_body = models.TextField(verbose_name="Блок в body (внизу)", blank=True, null=True)
    link_twitter = models.CharField(max_length=256, verbose_name="Ссылка на twitter", blank=True, null=True, editable=False)
    link_facebook = models.CharField(max_length=256, verbose_name="Ссылка на facebook", blank=True, null=True, editable=False)
    link_lj = models.CharField(max_length=256, verbose_name="Ссылка на lj", blank=True, null=True, editable=False)
    link_instagram = models.CharField(max_length=256, verbose_name="Ссылка на instagram", blank=True, null=True, editable=False)
    link_vk = models.CharField(max_length=256, verbose_name="Ссылка на вконтакте", blank=True, null=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Счетчики Яндекс и другие"
        db_table = 'contacts_contacts'
