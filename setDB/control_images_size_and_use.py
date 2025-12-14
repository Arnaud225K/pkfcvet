#-*- coding: utf-8 -*-
#соединиться с БД
from sqlalchemy import create_engine
#определим нашу таблицу внутри каталога MetaData
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Boolean,Text

import os
import shutil
import getpass
from PIL import Image
# import Image
USER_NAME = getpass.getuser()

if USER_NAME == 'andrey':
    PROJECT_NAME = 'pkfcvet'
    PATH_PROJECT = '/home/'+ USER_NAME +'/PycharmProjects/' + PROJECT_NAME
else:
    PATH_PROJECT = '/home/pkfcvet/pkfcvet'

MEDIA_ROOT = PATH_PROJECT + '/www/media/'

MEDIA_ROOT_LOAD = MEDIA_ROOT+'uploads/images/load/'
MEDIA_ROOT_MAIN = MEDIA_ROOT+'uploads/images/'
MEDIA_ROOT_TRACH = PATH_PROJECT + '/auto_trash/'
MEDIA_ROOT_TRACH_LOAD = PATH_PROJECT + '/auto_trash/load/'
MEDIA_ROOT_BACKUP = PATH_PROJECT + '/auto_backup/'

RESULT_FILE_NAME = PATH_PROJECT + '/result_control_images.txt'

WIDTH_PRODUCT = 500
WIDTH_MENU = 500
WIDTH_NEWS = 720
# WIDTH_PORTFOLIO = 409
# WIDTH_SPEC = 640


engine = create_engine("mysql://pkfcvet:LvKtHM9tKUSBmtAH@pkfcvet.ru/pkfcvet?host=pkfcvet.ru?charset=utf8")

metadata = MetaData()
product_table = Table('menu_product', metadata,
    Column('id', Integer, primary_key=True),
    Column('slug', String(1024)),
    Column('image', String(100)),
    Column('image_dop', String(100)),
    Column('isHidden', Boolean),
)

menu_table = Table('menu_menucatalog', metadata,
    Column('id', Integer, primary_key=True),
    Column('slug', String(1024)),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

news_table = Table('News_news', metadata,
    Column('id', Integer, primary_key=True),
    Column('name_lat', String(1024)),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

portfolio_table = Table('portfolio_portfolio', metadata,
    Column('id', Integer, primary_key=True),
    Column('name_lat', String(1024)),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

sertificats_table = Table('Sertificats_sertificats', metadata,
    Column('id', Integer, primary_key=True),
    Column('name_lat', String(1024)),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

slider_table = Table('slider_slider', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', String(1024)),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

specpredlozhenie_table = Table('SpecPredlozhenie_specpredlozhenie', metadata,
    Column('id', Integer, primary_key=True),
    Column('name_lat', String(1024)),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

textblockmenu_table = Table('TextBlockMenu_textblockmenu', metadata,
    Column('id', Integer, primary_key=True),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

textbloclurl_table = Table('TextBlockUrl_textblockurl', metadata,
    Column('id', Integer, primary_key=True),
    Column('image', String(100)),
    Column('isHidden', Boolean),
)

metadata.create_all(engine)

images_err_path = []
images_err_size_path = []
images_good_path = []
result_txt = []

count_err = 0
count_warn = 0
count_size_small = 0


class Menu(object):
    def __init__(self, slug, image, isHidden):
        self.slug = slug
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return self.slug

    def __repr__(self):
        return "<Menu('%s','%s', '%s','%s','%s')>" % (self.id, self.slug, self.image, self.isHidden)


class Product(object):
    def __init__(self, slug, image, image_dop, isHidden):
        self.slug = slug
        self.image = image
        self.image_dop = image_dop
        self.isHidden = isHidden

    def get_slug(self):
        return self.slug

    def __repr__(self):
        return "<Product('%s','%s', '%s','%s','%s')>" % (self.id, self.slug, self.image, self.image_dop, self.isHidden)


class News(object):
    def __init__(self, name_lat, image, image_dop, isHidden):
        self.name_lat = name_lat
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return self.name_lat

    def __repr__(self):
        return "<News('%s','%s', '%s','%s','%s')>" % (self.id, self.name_lat, self.image, self.image_dop, self.isHidden)


class Portfolio(object):
    def __init__(self, name_lat, image, image_dop, isHidden):
        self.name_lat = name_lat
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return self.name_lat

    def __repr__(self):
        return "<Portfolio('%s','%s', '%s','%s','%s')>" % (self.id, self.name_lat, self.image, self.image_dop, self.isHidden)


class Sertificats(object):
    def __init__(self, slug, image, image_dop, isHidden):
        self.slug = slug
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return self.name_lat

    def __repr__(self):
        return "<Sertificats('%s','%s', '%s','%s','%s')>" % (self.id, self.slug, self.image, self.image_dop, self.isHidden)


class Slider(object):
    def __init__(self, url, image, image_dop, isHidden):
        self.url = url
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return self.url

    def __repr__(self):
        return "<Slider('%s','%s', '%s','%s','%s')>" % (self.id, self.url, self.image, self.image_dop, self.isHidden)


class SpecPredlozhenie(object):
    def __init__(self, slug, image, image_dop, isHidden):
        self.slug = slug
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return self.name_lat

    def __repr__(self):
        return "<SpecPredlozhenie('%s','%s', '%s','%s','%s')>" % (self.id, self.slug, self.image, self.image_dop, self.isHidden)


class TextBlockMenu(object):
    def __init__(self, slug, image, image_dop, isHidden):
        self.slug = slug
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return ""

    def __repr__(self):
        return "<TextBlockMenu('%s','%s', '%s','%s','%s')>" % (self.id, self.slug, self.image, self.image_dop, self.isHidden)


class TextBlockUrl(object):
    def __init__(self, slug, image, image_dop, isHidden):
        self.slug = slug
        self.image = image
        self.isHidden = isHidden

    def get_slug(self):
        return ""

    def __repr__(self):
        return "<TextBlockUrl('%s','%s', '%s','%s','%s')>" % (self.id, self.slug, self.image, self.image_dop, self.isHidden)

from sqlalchemy.orm import mapper
mapper(Product, product_table)
mapper(Menu, menu_table)
mapper(News, news_table)
mapper(Portfolio, portfolio_table)
mapper(Sertificats, sertificats_table)
mapper(Slider, slider_table)
mapper(SpecPredlozhenie, specpredlozhenie_table)
mapper(TextBlockMenu, textblockmenu_table)
mapper(TextBlockUrl, textbloclurl_table)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

def my_print(tmp_str):
    print(tmp_str)
    result_txt.append(tmp_str)


def control_size_image(instance, image_path, etalon_width = None):
    global count_size_small
    global count_warn
    global count_err
    global images_good_path
    global images_err_path
    global images_err_size_path
    result = True
    result_not_found = False
    input_image_path = image_path.replace("%20"," ")
    if (not (input_image_path in images_err_path)) and (not (input_image_path in images_err_size_path)):
        if os.path.exists(input_image_path):
            if etalon_width:
                try:
                    original_image = Image.open(input_image_path)
                    width, height = original_image.size
                except:
                    result = False
                if result:
                    if width < etalon_width:
                        my_print("[WARN SM] Image bad size (width: "+str(width)+" ["+str(etalon_width)+"] - small): "+input_image_path + " (id: "+str(instance.id)+") slug: " +instance.get_slug()+")")
                        count_size_small +=1
                        images_err_size_path.append(input_image_path)
                    if width > etalon_width:
                        my_print("[WARN] Image bad size (width: "+str(width)+" ["+str(etalon_width)+"] - big): "+input_image_path + " (id: "+str(instance.id)+") slug: " +instance.get_slug()+")")
                        count_warn +=1
                        images_err_size_path.append(input_image_path)
                        tmp_name = os.path.basename(input_image_path)
                        #Копируем в backup
                        tmp_new_name = input_image_path.replace(MEDIA_ROOT_MAIN, MEDIA_ROOT_BACKUP)
                        shutil.copyfile(input_image_path, tmp_new_name)
                        #Проводим сжатие
                        img = Image.open(input_image_path)
                        try:
                            img.load()
                        except IOError:
                            pass # You can always log it to logger
                        img.thumbnail((etalon_width, 1000), Image.ANTIALIAS)
                        try:
                            img.save(input_image_path)
                        except:
                            try:
                                img.save(input_image_path, "JPEG")
                            except:
                                shutil.copyfile(tmp_new_name, input_image_path)
                                img.save(input_image_path, "PNG")


        else:
            my_print("[ERROR] Image not found: "+input_image_path + " (id: "+str(instance.id) + ") slug: " +instance.get_slug()+")")
            # try:
            #     if instance.image_dop and MEDIA_ROOT + instance.image_dop == input_image_path:
            #         instance.image_dop = None
            # except:
            #     pass
            if instance.image and MEDIA_ROOT + instance.image == input_image_path:
                instance.image = None

            result = False
            result_not_found = True
            count_err +=1
        if not result and not result_not_found:
            images_err_path.append(input_image_path)
        else:
            if not (input_image_path in images_good_path):
                images_good_path.append(input_image_path)
    else:
        result = False

    return result


def control_products():
    global images_good_path
    global images_err_path
    global images_err_size_path
    images_err_path = []
    images_err_size_path = []
    images_good_path = []

    my_print("=== CONTROL IMAGE PRODUCT ==")
    i = 0
    # for instance in session.query(Product).filter(Product.id<1000).filter(Product.isHidden == False):
    for instance in session.query(Product).filter(Product.isHidden == False):
        if i%10000 == 0:
            print i
        if instance.image:
            control_size_image(instance, MEDIA_ROOT + instance.image, WIDTH_PRODUCT)
        # if instance.image_dop:
        #     control_size_image(instance, MEDIA_ROOT + instance.image_dop, WIDTH_PRODUCT)
        i = i+1

    count_products = i
    i = 0
    # Механизм проверки основной директории
    my_print("==========================")
    images_fact_os = os.listdir(MEDIA_ROOT_LOAD)
    for item in images_fact_os:
        if os.path.isdir(MEDIA_ROOT_LOAD+item):
            continue
        if i%10000 == 0:
            print i
        if not (MEDIA_ROOT_LOAD+item in images_good_path) and not (MEDIA_ROOT_MAIN+item in images_good_path):
            my_print("Remove: " + MEDIA_ROOT_TRACH_LOAD+item)
            os.rename(MEDIA_ROOT_LOAD+item, MEDIA_ROOT_TRACH_LOAD+item)
        i = i+1



    my_print("==========================")
    my_print("ALL PRODUCTS DB: "+str(count_products))
    my_print("ALL IMAGES DB: "+str(len(images_good_path)))
    my_print("ALL IMAGES OS: "+str(i))
    print len(images_good_path)
    print("==========================")


def control_menus():
    global images_good_path
    global images_err_path
    global images_err_size_path

    i = 0
    count_products = 0
    images_err_path = []
    images_err_size_path = []
    images_good_path = []
    my_print("=== CONTROL IMAGE MENU ==")
    for instance in session.query(Menu).filter(Menu.isHidden == False):
        control_size_image(instance, MEDIA_ROOT + instance.image, WIDTH_MENU)
        i = i+1
    my_print("=== CONTROL IMAGE News ==")
    for instance in session.query(News).filter(News.isHidden == False):
        control_size_image(instance, MEDIA_ROOT + instance.image, WIDTH_NEWS)
        i = i+1
    # my_print("=== CONTROL IMAGE Portfolio ==")
    # for instance in session.query(Portfolio).filter(Portfolio.isHidden == False):
    #     control_size_image(instance, MEDIA_ROOT + instance.image, WIDTH_PORTFOLIO)
    #     i = i+1
    # my_print("=== CONTROL IMAGE Sertificats ==")
    # for instance in session.query(Sertificats).filter(Sertificats.isHidden == False):
    #     control_size_image(instance, MEDIA_ROOT + instance.image)
    #     i = i+1
    # my_print("=== CONTROL IMAGE Slider ==")
    # for instance in session.query(Slider).filter(Slider.isHidden == False):
    #     control_size_image(instance, MEDIA_ROOT + instance.image)
    #     i = i+1
    # my_print("=== CONTROL IMAGE SpecPredlozhenie ==")
    # for instance in session.query(SpecPredlozhenie).filter(SpecPredlozhenie.isHidden == False):
    #     control_size_image(instance, MEDIA_ROOT + instance.image, WIDTH_SPEC)
    #     i = i+1
    # my_print("=== CONTROL IMAGE TextBlockMenu ==")
    # for instance in session.query(TextBlockMenu).filter(TextBlockMenu.isHidden == False):
    #     control_size_image(instance, MEDIA_ROOT + instance.image)
    #     i = i+1
    # my_print("=== CONTROL IMAGE TextBlockUrl ==")
    # for instance in session.query(TextBlockUrl).filter(TextBlockUrl.isHidden == False):
    #     control_size_image(instance, MEDIA_ROOT + instance.image)
    #     i = i+1

    count_products = i
    i = 0
    my_print("==========================")
    images_fact_os = os.listdir(MEDIA_ROOT_MAIN)
    for item in images_fact_os:
        if os.path.isdir(MEDIA_ROOT_MAIN+item):
            continue
        if i%10000 == 0:
            print i
        # if not (MEDIA_ROOT_MAIN+item in images_good_path):
        #     my_print("Remove: " + MEDIA_ROOT_MAIN+item)
            # os.rename(MEDIA_ROOT_MAIN+item, MEDIA_ROOT_TRACH+item)
        i = i+1



    my_print("==========================")
    my_print("ALL POSITION DB: "+str(count_products))
    my_print("ALL IMAGES DB: "+str(len(images_good_path)))
    my_print("ALL IMAGES OS: "+str(i))
    print len(images_good_path)
    print("==========================")

#Контроль продукта
control_products()
control_menus()

# session.commit()

my_print("==========================")
my_print("Count ERROR: "+str(count_err))
my_print("Count WARN: "+str(count_warn))
my_print("Count WARN SM: "+str(count_size_small))

out = open(RESULT_FILE_NAME,"w+")
for tmp_str in result_txt:
    print tmp_str
    out.write(tmp_str+'\n')
out.close()




