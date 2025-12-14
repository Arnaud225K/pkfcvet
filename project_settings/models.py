import os

from django.db import models
from django.db.models.signals import post_delete, pre_save
from tinymce import models as tinymce_models


class ProjectSettings(models.Model):
	name = models.CharField(max_length=256, verbose_name="Название компании")
	site_name = models.CharField(max_length=256, verbose_name="Название сайта")

	text_head = models.TextField(verbose_name="Блок в head (внизу)", blank=True, null=True, default="", editable=False)
	text_body = models.TextField(verbose_name="Блок в body (внизу)", blank=True, null=True, default="", editable=False)

	tech_mail_server = models.CharField(max_length=256, verbose_name="Почтовый сервер (для отправки сообщений)", blank=True, null=True, default="", editable=False)
	tech_email = models.CharField(max_length=256, verbose_name="Почта для отправки сообщений", blank=True, null=True, default="", editable=False)
	tech_email_pass = models.CharField(max_length=256, verbose_name="Пароль почты для отправки сообщений", blank=True, default="", null=True, editable=False)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["id"]
		verbose_name_plural = "Настройки проекта"
