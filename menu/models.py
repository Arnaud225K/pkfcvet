from django.db import models
from django.db.models import Q 
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.db.models import Count

from tinymce import models as tinymce_models

from transliterate import translit
import os
from operator import itemgetter
from itertools import groupby
from django.db.models import Index
from django.db.models.functions import Upper

from typemenu.models import TypeMenu
from Marochnik.models import MarkaMetall
from GOST.models import GOST
from Sertificats.models import Sertificats
from checkout.models import Order, OrderItem


# --- MANAGERS ---

class ActiveMenuCatalogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isHidden=False)

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isHidden=False)

class FeaturedProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isHidden=False, is_featured=True)



class MenuCatalog(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название пункта")
    slug = models.CharField(max_length=255, unique=True, verbose_name="Название латинское", blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Родительский пункт", null=True, blank=True)
    typeMenu = models.ForeignKey(TypeMenu, on_delete=models.PROTECT, verbose_name="Тип меню", db_column='typemenu_id')
    name = models.CharField(max_length=255, unique=True, verbose_name="Название пункта")
    name_short = models.CharField(max_length=255, verbose_name="Название пункта (сокращенное)", blank=True, null=True)
    name_p = models.CharField(max_length=255, verbose_name="Название пункта (в винительном падеже)", blank=True, null=True)
    slug = models.CharField(max_length=255, unique=True, verbose_name="Название латинское", blank=True)
    order_number = models.FloatField(verbose_name="Порядковый номер", blank=True, null=True)
    name_title = models.CharField(max_length=1024, verbose_name="Название (в ед. числе)", blank=True)
    name_info = models.CharField(max_length=1024, verbose_name="Название (для поля консультация)", blank=True)
    price_title = models.CharField(max_length=256, verbose_name="Заголовок поля цена", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Родительский пункт", null=True, blank=True)
    typeMenu = models.ForeignKey(TypeMenu, on_delete=models.PROTECT, verbose_name="Тип меню", db_column='typemenu_id')
    catalog_childs_dop = models.ManyToManyField('self', verbose_name="Вложенные категории (дополнительные)",blank=True, symmetrical=False, related_name='parent_catalogs_dop')
    catalog_childs_dop_menu = models.ManyToManyField('self', verbose_name="Вложенные категории (дополнительные в меню)",blank=True, symmetrical=False, related_name='parent_catalogs_dop_menu')
    parent_catalog_dop = models.BooleanField(verbose_name="Родительская категория для вложенных (дополнительных)", blank=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    labelSizeA = models.CharField(max_length=256, verbose_name="Название размера А", blank=True, null=True, db_column='labelsizea')
    labelSizeAslug = models.CharField(max_length=256, verbose_name="Название размера А для фильтра (транслит)", blank=True, null=True, db_column='labelsizeaslug')
    labelSizeB = models.CharField(max_length=256, verbose_name="Название размера B", blank=True, null=True, db_column='labelsizeb')
    labelSizeBslug = models.CharField(max_length=256, verbose_name="Название размера B для фильтра (транслит)", blank=True, null=True, db_column='labelsizebslug')
    labelSizeC = models.CharField(max_length=256, verbose_name="Название размера C", blank=True, null=True, db_column='labelsizec')
    labelSizeCslug = models.CharField(max_length=256, verbose_name="Название размера C для фильтра (транслит)", blank=True, null=True, db_column='labelsizecslug')
    labelSizeD = models.CharField(max_length=256, verbose_name="Название размера D", blank=True, null=True, db_column='labelsized')
    labelSizeDslug = models.CharField(max_length=256, verbose_name="Название размера D для фильтра (транслит)", blank=True, null=True, db_column='labelsizedslug')
    labelSizeE = models.CharField(max_length=256, verbose_name="Название размера E", blank=True, null=True, db_column='labelsizee')
    labelSizeEslug = models.CharField(max_length=256, verbose_name="Название размера E для фильтра (транслит)", blank=True, null=True, db_column='labelsizeeslug')
    labelSizeF = models.CharField(max_length=256, verbose_name="Название размера F", blank=True, null=True, db_column='labelsizef')
    labelSizeFslug = models.CharField(max_length=256, verbose_name="Название размера F для фильтра (транслит)", blank=True, null=True, db_column='labelsizefslug')
    labelSizeL = models.CharField(max_length=256, verbose_name="Название размера L", blank=True, null=True, db_column='labelsizel')
    labelSizeLslug = models.CharField(max_length=256, verbose_name="Название размера L для фильтра (транслит)", blank=True, null=True, db_column='labelsizelslug')
    isHideMarka = models.BooleanField(verbose_name="Скрыть марку", blank=True, db_column='ishidemarka')
    isHideGOST = models.BooleanField(verbose_name="Скрыть ГОСТ", blank=True, db_column='ishidegost')
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True, null=True)
    oplata = models.TextField(verbose_name="Текст Оплата и отгрузка / блок head для меню с типом Информация", blank=True, null=True)
    dostavka = models.TextField(verbose_name="Текст Доставка/ блок body для меню с типом Информация", blank=True, null=True)
    comment = models.CharField(max_length=1024, verbose_name="Комментарий", blank=True, null=True)
    flagFooter = models.BooleanField(verbose_name="Флаг Footer", db_column='flagfooter')
    flagProduct = models.BooleanField(verbose_name="Выводим товары под текстом ?", default=False, db_column='flagproduct')
    title_main = models.CharField(max_length=1024, verbose_name="Заголовок страницы", blank=True, null=True)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True,help_text='Ключевые слова для SEO продвижения (через запятую). Мета тэг - keywords')
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True, help_text='Содержимое мета тэга - description')
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = models.Manager()
    active = ActiveMenuCatalogManager()

    @property
    def name_little(self):
        if self.name_short:
            return self.name_short
        return self.name

    def __str__(self):
        name_str = self.name
        if self.parent:
            name_str += f" ({self.parent.name})"
        return name_str

    class Meta:
        ordering = ["-order_number", "name"]
        verbose_name_plural = "Меню/Каталог"
        db_table = 'menu_menucatalog'
        indexes = [
            Index(Upper('slug'), name='menucatalog_slug_upper_idx'),
        ]

    def get_absolute_url(self):
        return reverse('menu:menu_catalog_detail', kwargs={'menu_slug': self.slug})
    
    
    def get_child_menu(self):
        """Retourne les enfants directs. Utilise les données pré-chargées si disponibles."""
        if hasattr(self, 'prefetched_children'):
            return self.prefetched_children
        return self.menucatalog_set.filter(isHidden=False)

    def get_child_menu_dop(self):
        """Retourne les enfants directs ET les enfants supplémentaires."""
        children = list(self.get_child_menu())
        
        if self.parent_catalog_dop:
            if hasattr(self, 'prefetched_dop_children'):
                children.extend(self.prefetched_dop_children)
            else:
                children.extend(list(self.catalog_childs_dop.all()))
        
        seen = set()
        return [x for x in children if not (x.id in seen or seen.add(x.id))]
    
    def get_child_menu_dops(self):
        """Retourne les enfants directs ET les enfants supplémentaires DU MENU."""
        children = list(self.get_child_menu())
        
        if hasattr(self, 'prefetched_dop_menu_children'):
             children.extend(self.prefetched_dop_menu_children)
        else:
             children.extend(list(self.catalog_childs_dop_menu.all()))

        seen = set()
        return [x for x in children if not (x.id in seen or seen.add(x.id))]

    def get_parent_menu(self):
        """Remonte l'arbre pour trouver le parent racine. Ne fera pas de requêtes si bien pré-chargé."""
        current = self
        while current.parent:
            current = current.parent
        return current

    def get_list_product(self):
        return Product.objects.filter(catalog=self.id, isHidden=False).only('name_main', 'slug', 'image')

    def get_list_product_count(self):
        count = Product.objects.filter(
            Q(catalog=self) | Q(catalogOne=self) |
            Q(catalogTwo=self) | Q(catalogThree=self),
            isHidden=False
        ).values('id').distinct().count()
        return count

    def get_list_marka(self):
        return Product.objects.filter(catalog=self.id, isHidden=False).values("marka__name").annotate(query_count=Count("marka")).order_by('marka__name')

    def get_list_marka_all(self):
        return list(map(itemgetter(0), groupby(Product.objects.filter(catalog=self.id, isHidden=False).values('marka__name', 'marka__name_lat', 'marka__hiddenSite').order_by('marka__name'))))

    def get_list_gost_all(self):
        return list(map(itemgetter(0), groupby(Product.objects.filter(catalog=self.id, isHidden=False).values('gost__number', 'gost__number_lat').order_by('gost__number'))))

    def get_sertificates(self):
        product_sertificates = Product.objects.filter(
            catalog=self, isHidden=False, sertificate__isnull=False
        ).select_related('sertificate').values_list('sertificate', flat=True)
        
        sertificat_ids = list(set(product_sertificates))[:11]
        return Sertificats.objects.filter(id__in=sertificat_ids)

    def get_main_sertificates(self):
        sub_categories = self.get_child_menu()
        sub_category_ids = [item.id for item in sub_categories]
        
        product_sertificates = Product.objects.filter(
            catalog_id__in=sub_category_ids, isHidden=False, sertificate__isnull=False
        ).select_related('sertificate').values_list('sertificate', flat=True)
        
        sertificat_ids = list(set(product_sertificates))[:20]
        return Sertificats.objects.filter(id__in=sertificat_ids)

    def get_metall_categories_similar(self):
        return MenuCatalog.objects.filter(parent=self, isHidden=False)[:4]


class Product(models.Model):
    order_number = models.FloatField(verbose_name="Приоритет (Порядковый номер)", blank=True, null=True)
    name_main = models.CharField(max_length=1024, verbose_name="Название", blank=True, null=True)
    name_info = models.CharField(max_length=1024, verbose_name="Название (для поля консультация разделов 'Производство','Услуги','Спецпредложения')", blank=True)
    slug = models.CharField(max_length=1024, verbose_name="Название латинское", blank=True, null=True)
    catalog = models.ForeignKey(MenuCatalog, on_delete=models.PROTECT, verbose_name="Категория металлопроката")
    catalogOne = models.ForeignKey(MenuCatalog, on_delete=models.SET_NULL, verbose_name="Категория металлопроката 1", blank=True, null=True, related_name="Product_catalogOne", db_column='catalogone_id')
    catalogTwo = models.ForeignKey(MenuCatalog, on_delete=models.SET_NULL, verbose_name="Категория металлопроката 2", blank=True, null=True, related_name="Product_catalogTwo", db_column='catalogtwo_id')
    catalogThree = models.ForeignKey(MenuCatalog, on_delete=models.SET_NULL, verbose_name="Категория металлопроката 3", blank=True, null=True, related_name="Product_catalogThree", db_column='catalogthree_id')
    size_a = models.CharField(max_length=256, verbose_name="Размер A", blank=True, null=True)
    size_b = models.CharField(max_length=256, verbose_name="Размер B", blank=True, null=True)
    size_c = models.CharField(max_length=256, verbose_name="Размер C", blank=True, null=True)
    size_d = models.CharField(max_length=256, verbose_name="Размер D", blank=True, null=True)
    size_e = models.CharField(max_length=256, verbose_name="Размер E", blank=True, null=True)
    size_f = models.CharField(max_length=256, verbose_name="Размер F", blank=True, null=True)
    size_l = models.CharField(max_length=256, verbose_name="Размер L", blank=True, null=True)
    marka = models.ForeignKey(MarkaMetall, on_delete=models.SET_NULL, verbose_name="Марка", blank=True, null=True)
    gost = models.ForeignKey(GOST, on_delete=models.SET_NULL, verbose_name="ГОСТ", blank=True, null=True)
    available = models.CharField(max_length=256, verbose_name="Наличие", blank=True, null=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=9, decimal_places=2)
    ed_izm = models.CharField(max_length=256, verbose_name="Единицы измерения", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', verbose_name="Картинка", blank=True, null=True)
    image_dop = models.ImageField(upload_to='uploads/images', verbose_name="Картинка (дополнительная)", blank=True, null=True)
    description = tinymce_models.HTMLField(verbose_name="Описание", blank=True, null=True)
    vendor = models.CharField(max_length=256, verbose_name="Производитель", blank=True, null=True)
    vendor_country = models.CharField(max_length=256, verbose_name="Страна производителя", blank=True, null=True)
    method_of_manufacture = models.CharField(max_length=256, verbose_name="Способ изготовления", blank=True, null=True)
    sertificate = models.ForeignKey(Sertificats, on_delete=models.SET_NULL, verbose_name="Сертификат", blank=True, null=True)
    title_main = models.CharField(max_length=1024, verbose_name="Заголовок страницы", blank=True, null=True)
    keywords = models.TextField(verbose_name="Ключевые слова (мета)", blank=True, null=True)
    keywords_description = models.TextField(verbose_name="Описание (мета)", blank=True, null=True)
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()

    def __str__(self):
        return self.name_main or 'без названия'

    class Meta:
        ordering = ["-order_number"]
        verbose_name_plural = "Продукт"
        indexes = [
            Index(Upper('slug'), name='product_slug_upper_idx'),
        ]

    def get_absolute_url(self):
        return reverse('menu:product_detail', kwargs={'product_slug': self.slug})
    
    @property
    def name(self):
        name_product = ""
        if self.name_main:
            name_product = self.name_main
        else:
            name_product = self.catalog.name
            if self.marka:
                name_product += " " + self.marka.name
            if self.gost:
                name_product += " " + self.gost.number
            if self.size_a:
                name_product += " " + str(self.size_a)
            if self.size_b:
                name_product += "x" + str(self.size_b)
            if self.size_c:
                name_product += "x" + str(self.size_c)
            if self.size_d:
                name_product += "x" + str(self.size_d)
            if self.size_e:
                name_product += "x" + str(self.size_e)
            if self.size_f:
                name_product += "x" + str(self.size_f)
            if self.size_l:
                name_product += "x" + str(self.size_l)
        return name_product

    @property
    def name_service(self):
        name_product = ""
        is_size = False
        if self.catalog.name_info:
            name_product = self.catalog.name_info
        else:
            name_product = self.catalog.name
        if self.size_a:
            name_product += " " + self.get_size_a()
            is_size = True
        if self.size_b:
            name_product += "x" + self.get_size_b()
            is_size = True
        if self.size_c:
            name_product += "x" + self.get_size_c()
            is_size = True
        if self.size_d:
            name_product += "x" + self.get_size_d()
            is_size = True
        if self.size_e:
            name_product += "x" + self.get_size_e()
            is_size = True
        if self.size_f:
            name_product += "x" + self.get_size_f()
            is_size = True
        if self.size_l:
            name_product += "x" + self.get_size_l()
            is_size = True
        if self.marka:
            name_product += " " + self.marka.name
        if self.gost:
            name_product += " " + self.gost.number
        return name_product

    def get_image(self):
        if self.image:
            return self.image
        return self.catalog.image

    def get_size_a(self):
        if not self.catalog.labelSizeA:
            return ""
        size_a = f"{self.size_a}"
        if size_a.endswith(".0"):
            size_a = size_a[:-2]
        return size_a

    def get_size_b(self):
        if not self.catalog.labelSizeB:
            return ""
        size_b = f"{self.size_b}"
        if size_b.endswith(".0"):
            size_b = size_b[:-2]
        return size_b

    def get_size_c(self):
        if not self.catalog.labelSizeC:
            return ""
        size_c = f"{self.size_c}"
        if size_c.endswith(".0"):
            size_c = size_c[:-2]
        return size_c

    def get_size_d(self):
        if not self.catalog.labelSizeD:
            return ""
        size_d = f"{self.size_d}"
        if size_d.endswith(".0"):
            size_d = size_d[:-2]
        return size_d

    def get_size_e(self):
        if not self.catalog.labelSizeE:
            return ""
        size_e = f"{self.size_e}"
        if size_e.endswith(".0"):
            size_e = size_e[:-2]
        return size_e

    def get_size_f(self):
        if not self.catalog.labelSizeF:
            return ""
        size_f = f"{self.size_f}"
        if size_f.endswith(".0"):
            size_f = size_f[:-2]
        return size_f

    def get_size_l(self):
        if not self.catalog.labelSizeL:
            return ""
        size_l = f"{self.size_l}"
        if size_l.endswith(".0"):
            size_l = size_l[:-2]
        return size_l
    
    def results(request):
        search_text = request.GET.get('q', '')
        results = Product.objects.filter(name__icontains=search_text)
        return results

    def cross_sells(self):
        
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        products = Product.objects.filter(orderitem__in=order_items).distinct()
        return products

    def cross_sells_user(self):
        
        users = settings.AUTH_USER_MODEL.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self)
        products = Product.objects.filter(orderitem__in=items).distinct()
        return products

    def cross_sells_hybrid(self):
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = settings.AUTH_USER_MODEL.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(
            Q(order__in=orders) | Q(order__user__in=users)
        ).exclude(product=self)
        products = Product.objects.filter(orderitem__in=items).distinct()
        return products
    
    def control_size(self, size_value):
        try:
            size_value = size_value.replace(".", ",")
        except:
            size_value = str(size_value).replace(".", ",")
        if size_value[-2:] == ",0":
            size_value = size_value[:-2]
        return size_value


    def set_slug(self):
        name_product = ""
        if self.size_a:
            self.size_a = self.control_size(self.size_a)
        if self.size_b:
            self.size_b = self.control_size(self.size_b)
        if self.size_c:
            self.size_c = self.control_size(self.size_c)
        if self.size_d:
            self.size_d = self.control_size(self.size_d)
        if self.size_e:
            self.size_e = self.control_size(self.size_e)
        if self.size_f:
            self.size_f = self.control_size(self.size_f)
        if self.size_l:
            self.size_l = self.control_size(self.size_l)
        if self.name_main:
            name_product = translit(self.name_main, "ru", reversed=True).replace(u" ", "_").replace("+", "-").replace(";", "").replace(":", "").replace(".", "-").replace(
                " ", "_").replace(",", "").replace("'", "").replace("(", "").replace(")", "").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
        else:
            name_product = translit(self.catalog.name, "ru", reversed=True).replace(u" ", "_").replace(" ", "_").replace(",", "").replace(
                "'", "").replace("(", "").replace(")", "").replace("!", "").replace("\'", "").replace("\\", "").replace("/", "_").lower()
            if self.marka:
                name_product += "_" + self.marka.name_lat
            if self.gost:
                name_product += "_" + self.gost.number_lat
            if self.size_a:
                name_product += "_" + str(self.size_a)
            if self.size_b:
                name_product += "x" + str(self.size_b)
            if self.size_c:
                name_product += "x" + str(self.size_c)
            if self.size_d:
                name_product += "x" + str(self.size_d)
            if self.size_e:
                name_product += "x" + str(self.size_e)
            if self.size_f:
                name_product += "x" + str(self.size_f)
            if self.size_l:
                name_product += "x" + str(self.size_l)
            name_product = name_product.replace(".0x", "x")
            if name_product[-2:] == ".0":
                name_product = name_product[:-2]
            name_product = name_product.replace(".", "-")
            name_product = name_product.replace(",", "-")
            name_product = name_product.replace("+", "-")
        self.slug = name_product


class tableProductDop(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="Product")
    product_dop = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Дополнительный продукт", related_name="Product_dop")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        product_name = self.product.name_main or ''
        product_dop_name = self.product_dop.name_main or ''
        return f'{product_name} - {product_dop_name}'

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Таблица дополнительных продуктов"


class ProductUsluga(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    usluga = models.ForeignKey(MenuCatalog, on_delete=models.CASCADE, verbose_name="Услуга")
    isHidden = models.BooleanField(verbose_name="Скрыть", blank=True, db_column='ishidden')

    def __str__(self):
        product_name = self.product.name_main or ''
        usluga_name = self.usluga.name or ''
        return f'{product_name} - {usluga_name}'

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Продукт - Услуга"


@receiver(post_delete, sender=MenuCatalog)
def delete_menucatalog_image(sender, instance, **kwargs):
    if instance.image and os.path.exists(instance.image.path):
        os.remove(instance.image.path)

@receiver(pre_save, sender=MenuCatalog)
def update_menucatalog_slug_and_image(sender, instance, **kwargs):
    if not instance.slug and instance.name:
        slug = ""
        if instance.parent and instance.parent.slug:
            slug += instance.parent.slug + '__'
        slug += translit(instance.name, "ru", reversed=True).replace(" ", "_").lower()
        import re
        instance.slug = re.sub(r'[^\w-]', '_', slug)

    if instance.pk:
        try:
            old_instance = MenuCatalog.objects.get(pk=instance.pk)
            if old_instance.image and (not instance.image or old_instance.image.path != instance.image.path):
                if os.path.exists(old_instance.image.path):
                    os.remove(old_instance.image.path)
        except MenuCatalog.DoesNotExist:
            pass

@receiver(pre_save, sender=Product)
def generate_product_slug(sender, instance, **kwargs):
    instance.set_slug()