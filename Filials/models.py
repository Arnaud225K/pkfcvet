from django.db import models
from tinymce import models as tinymce_models


class Filials(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_p = models.CharField(max_length=1024, verbose_name="Название (в предложеном падеже)", blank=True, null=True)
    subdomain_name = models.CharField(max_length=1024, verbose_name="Название поддомена")
    phone = models.CharField(max_length=1024, verbose_name="Телефон", blank=True, null=True)
    phone_yclid = models.CharField(max_length=1024, verbose_name="Телефон (yclid)", blank=True, null=True)
    phone_gclid = models.CharField(max_length=1024, verbose_name="Телефон (gclid)", blank=True, null=True)
    email = models.CharField(max_length=256, verbose_name="Электронная почта", blank=True, null=True)
    email_yclid = models.CharField(max_length=256, verbose_name="Электронная почта (yclid)", blank=True, null=True)
    email_gclid = models.CharField(max_length=256, verbose_name="Электронная почта (gclid)", blank=True, null=True)
    phone_dop = models.CharField(max_length=1024, verbose_name="Телефон (дополнительный)", blank=True, null=True)
    fax = models.CharField(max_length=1024, verbose_name="Факс", blank=True, null=True, editable=False)
    address = models.CharField(max_length=2048, verbose_name="Адрес", blank=True, null=True)
    rezhim = models.CharField(max_length=1024, verbose_name="Режим работы", blank=True, null=True)
    req = tinymce_models.HTMLField(verbose_name="Реквизиты", blank=True, null=True)
    comment = tinymce_models.HTMLField(verbose_name="Текст", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True, editable=False)
    is_main = models.BooleanField(verbose_name="Отображается без поддомена (по умолчанию)", blank=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')
    geo = models.CharField(max_length=1024, verbose_name="Код карты", blank=True, null=True)
    text_head_filial = models.TextField(verbose_name="Блок в head для филиала (внизу)", blank=True, null=True, default="")
    text_body_filial = models.TextField(verbose_name="Блок в body для филиала (внизу)", blank=True, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = u"Филиалы (Города)"
        db_table = 'filials_filials'


    def phone_href(self):
        return self.phone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")


    def phone_dop_href(self):
        return self.phone_dop.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

    # def phone(self):
    #     if request.session.get(CONTACTS_SESSION_KEY, '') == 'yclid':
    #         return self.phone_yclid
    #     if request.session.get(CONTACTS_SESSION_KEY, '') == 'gclid':
    #         return self.phone_gclid
    #     return '8 800'

    # def email(self):
    #     if request.session.get(CONTACTS_SESSION_KEY, '') == 'yclid':
    #         return self.email_yclid
    #     if request.session.get(CONTACTS_SESSION_KEY, '') == 'gclid':
    #         return self.email_gclid
    #     return 'info@pkf'
