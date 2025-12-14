from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models
from transliterate import translit

import os


class NewsType(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Типы новостей/статей"


class News(models.Model):
    order_number = models.IntegerField(verbose_name="Порядковый номер", blank=True, null=True)
    type = models.ForeignKey(NewsType, on_delete=models.PROTECT, verbose_name="Тип новости/статьи")
    name = models.CharField(max_length=1024, verbose_name="Название")
    name_lat = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True)
    articles_flag = models.BooleanField(verbose_name="Флаг - статьей", blank=True)
    nameLatCat_1 = models.CharField(max_length=1024, verbose_name="Название лат. каталога статьи", blank=True, null=True, db_column='namelatcat_1')
    nameLatCat_2 = models.CharField(max_length=1024, verbose_name="Название лат. каталога статьи", blank=True, null=True, db_column='namelatcat_2')
    nameLatProd_1 = models.CharField(max_length=1024, verbose_name="Название лат. продукта статьи", blank=True, null=True, db_column='namelatprod_1')
    nameLatProd_2 = models.CharField(max_length=1024, verbose_name="Название лат. продукта статьи", blank=True, null=True, db_column='namelatprod_2')
    date = models.DateTimeField(verbose_name='Дата')
    description = tinymce_models.HTMLField(verbose_name="Описание")
    text = tinymce_models.HTMLField(verbose_name="Текст")
    title_main = models.CharField(max_length=1024, verbose_name="Заголовок страницы", blank=True, null=True)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True, help_text='Ключевые слова для SEO продвижения (через запятую). Мета тэг - keywords')
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, help_text='Содержимое мета тэга - description')
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка новости", blank=True, null=True)
    isMain = models.BooleanField(verbose_name="Показывать в нижней панели", db_column="ismain")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')
    video = models.CharField(max_length=4096, verbose_name="Видео на Youtube", blank=True, null=True)
    isHiddenVideo = models.BooleanField(verbose_name="Не показывать видео", blank=True, db_column="ishiddenvideo")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.articles_flag:
            # Utiliser le nouveau namespace 'articles'
            return reverse('articles:articles_detail', kwargs={'articles_slug': self.name_lat})
        else:
            # Le namespace 'news' reste correct
            return reverse('news:news_detail', kwargs={'news_slug': self.name_lat})

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Новости/статьи"
        db_table = 'news_news'



@receiver(post_delete, sender=News)
def delete_news_image(sender, instance, **kwargs):
    """ Supprime le fichier image lorsque l'objet News est supprimé. """
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=News)
def update_news_image_and_slug(sender, instance, **kwargs):
    """ Met à jour le slug et supprime l'ancienne image si elle change. """
    if not instance.name_lat and instance.name:
        slug_base = translit(instance.name, "ru", reversed=True)
        instance.name_lat = "".join(c if c.isalnum() or c in "-_" else "_" for c in slug_base).lower()

    if not instance.pk:
        return

    try:
        old_instance = News.objects.get(pk=instance.pk)
    except News.DoesNotExist:
        return

    if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
        if os.path.exists(old_instance.image.path):
            os.remove(old_instance.image.path)