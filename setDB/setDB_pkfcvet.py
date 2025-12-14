#-*- coding: utf-8 -*-
'''
Created on 03.07.2012

@author: andrey
'''
import sys
import xlrd
from PyQt4 import QtCore, QtGui, Qt, uic

import locale
import re


CONTROL_CODE = "73aoF6N"


# 5.0|1.0|Труба бесшовная 108х4|108.0|4.0||||||09Г2С|ГОСТ 11|+|63430.0|тн|http:/png|http://www|Описание|Производитель|Россия|Способ изготовления|36.0|1.0|1.0|2.0|3.0|4.0|33.0|34.0|35.0|36.0
COLUMN_ID = 0
COLUMN_ORDER = 1
COLUMN_NAME = 2
COLUMN_SIZE_A = 3
COLUMN_SIZE_B = 4
COLUMN_SIZE_C = 5
COLUMN_SIZE_D = 6
COLUMN_SIZE_E = 7
COLUMN_SIZE_F = 8
COLUMN_SIZE_L = 9
COLUMN_MARKA = 10
COLUMN_GOST = 11
COLUMN_AVAILABLE = 12
COLUMN_PRICE = 13
COLUMN_ED_IZM = 14
COLUMN_IMAGE_1 = 15
COLUMN_IMAGE_2 = 16
COLUMN_DESCRIPTION = 17
COLUMN_VENDOR = 18
COLUMN_COUNTRY_VENDOR = 19
COLUMN_METHOD = 20
COLUMN_CATEGORY_ID = 21
COLUMN_SERTIFICATE_ID = 22
COLUMN_PRODUCT_1_ID = 23
COLUMN_PRODUCT_2_ID = 24
COLUMN_PRODUCT_3_ID = 25
COLUMN_PRODUCT_4_ID = 26
COLUMN_USLUGA_1_ID = 27
COLUMN_USLUGA_2_ID = 28
COLUMN_USLUGA_3_ID = 29
COLUMN_USLUGA_4_ID = 30


#Для программных целей (виртуальные колонки)
COLUMN_IMAGE_1_HTTP = -2
COLUMN_IMAGE_2_HTTP = -1
COLUMN_IMAGE_1_TECH_NAME = -4
COLUMN_IMAGE_2_TECH_NAME = -3





'''DATA_FLAG = 1 # Если 1, то ввод данных, иначе заполнение ГОСТ и марка для данной категории

if(DATA_FLAG==1):
    SET_DATA = True
    SET_PARAMETRS=False
else:
    SET_DATA = False
    SET_PARAMETRS=True'''
SET_DATA = True
SET_PARAMETRS=True

#SET_DATA = False
#SET_PARAMETRS=False

reload(sys)
locale.setlocale(locale.LC_ALL, '')
sys.setdefaultencoding('utf-8')
#
# class Product():
#     def __init__(self):
# 		self.id_product = 0
# 		self.priority = 0
# 		self.name = ""
# 		self.sizeA = 0
# 		self.sizeB = 0
# 		self.sizeC = 0
# 		self.sizeD = 0
# 		self.gost = 0
# 		self.marka = 0
# 		self.price = 0
# 		self.type = 0


class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.errConnect = False
        self.errMarkaFlag = False
        super(MainWindow, self).__init__()    
        uic.loadUi("setDB_pkfcvet.ui", self)
        self.fileName = ""
        # Окно по центру
        Desktop = QtGui.QApplication.desktop()
        x = (Desktop.width() - self.width()) // 2
        y = (Desktop.height() - self.height()) // 2
        self.move(x, y)

        # скрытие не нужных кнопок

        self.label_2.setVisible(False)
        self.pushButton.setVisible(True)
        self.pushButton_2.setVisible(False)
        self.spinBoxNumber.setVisible(False)
        self.spinBoxType.setVisible(False)

        #Подключение к БД
        self.db = Qt.QSqlDatabase.addDatabase("QMYSQL");
        self.db.setHostName("pkfcvet.ru");
        # self.db.setHostName("localhost");
        self.db.setDatabaseName("pkfcvet");
        self.db.setUserName("pkfcvet");
        self.db.setPassword("LvKtHM9tKUSBmtAH");
        #Для загрузки картинок
        # self.server = "127.0.0.1:8020"
        self.server = "pkfcvet.ru"
        if(self.db.open() == False):
            self.showMessageError('ОШИБКА! Невозможно подключиться к базе данных продукции!\nПроверьте подключение компьютера к сети и попробуйте еще раз!\nВ случае наличия сети и повторения этого сообщения\nсвяжитесь с разработчиком или поставщиком.')
            self.errConnect = True
            return
        self.model=Qt.QSqlTableModel(self)

        self.dictMarka = {}
        self.dictType = {}
        self.dictGost = {}

        self.dictTypeGost={}
        self.dictTypeMarka={}

        self.import_image_list = []


        self.model.setTable("Marochnik_markametall")
        self.model.select()
        for i in range(self.model.rowCount()):
            #print self.model.record(i).value(3).toString()
            key = unicode(self.model.record(i).value(3).toString().replace(' ','')).upper()
            value = self.model.record(i).value(0).toInt()[0]
            self.dictMarka[key] = value

            #print (key)

        self.model.setTable("menu_menucatalog")
        self.model.select()
        for i in range(self.model.rowCount()):
            value = str(self.model.record(i).value(10).toString())
            key = self.model.record(i).value(0).toInt()[0]
            self.dictType[key] = key
            # print (key)

        self.model.setTable("GOST_gost")
        self.model.select()
        for i in range(self.model.rowCount()):
            key = str(self.model.record(i).value(3).toString()).replace(' ','')
            value = self.model.record(i).value(0).toInt()[0]
            self.dictGost[key] = value
            # print (key)
            # print (value)

            #print self.dictType

    
    "Закрытие окна"              
    def closeEvent(self,event):
        '''
        Захотели закрыть главное окно
        '''
        Answer = QtGui.QMessageBox(QtGui.QMessageBox.Information,\
                        "Система ввода продукции","Вы уверены, что хотите закончить работу?",\
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No ).exec_()
            
        if Answer == QtGui.QMessageBox.No:
            event.ignore()
            return
        event.accept()

        
    "Открытие файла"
    def openFile(self):            
        self.dialog = QtGui.QFileDialog()
        self.fileName = self.dialog.getOpenFileName(self, 'Выбор файла для загрузки', "", "Excel Files *.xls (*.xls)")
        if self.fileName:
            self.lineEdit.clear()
            self.lineEdit.insert(self.fileName)
            
    "Импорт файла в БД (обработчик нажатия кнопки)"
    def importDB(self, flag_marka=None):
        self.fileName = self.lineEdit.text()
        if(self.fileName != ""):
            if(self.loadXLS(flag_marka)==False):
                if not flag_marka:
                    self.showMessageError('ОШИБКА! Неверная структура входного файла (Строка № '+str(self.errStr)+')\nУстраните ошибку и попробуйте еще раз.')
                    #print("ERROR "+str(self.errStr+1))
                return
            # return
            if(SET_DATA):
                if not flag_marka:
                    self.setDataDB()
                    self.showMessageInfo('Информация успешно добавлена в базу данных продукции!')
        else:
            self.showMessageError('ОШИБКА! Не выбран файл для загрузки')
            
    "Загрузка файла Excel"
    def loadXLS(self, flag_marka):
        book = xlrd.open_workbook(self.fileName)
        s = book.sheet_by_index(0)
        self.dataLoad = []
        index_row = 0
        for row in range(s.nrows):
            values=[]
            for col in range(s.ncols):
                values.append(str(s.cell(row,col).value))
            # print '|'.join((values))
            # print values[0]
            self.dataLoad.append(values)
        # return

        if(self.formatType(flag_marka)== False):
            return False
        
    #функцимя очистки пустых элементов массива    
    def _my_clear_empty_element(self,array):
        res_array = []
        for i in range(0,len(array)):
            if(array[i] != ""):
                res_array.append(array[i])
        return res_array
    
    "Форматирование загруженных данных в соответствии с указанным типом"
    def controlFormat(self):
        self.rezDataFormat = []
        for i in range(len(self.dataFormat)):
            self.rezDataFormat.append([])
            for j in range(len(self.dataFormat[i])):
                if(j==1):
                    rx = re.compile("[xXхХн*-]")
                    tmpArr = self._my_clear_empty_element(re.split(rx,self.dataFormat[i][j]))
                    if(len(tmpArr)>0 and len(tmpArr)<=3):
                        for k in range(len(tmpArr)):
                            tmpArr[k] = tmpArr[k].replace(",",".")
                            try:
                                a=float(tmpArr[k])
                            except:
                                print ("ERROR FLOAT").encode('cp1251')
                                self.errStr = i
                                return False
                                
                            self.rezDataFormat[i].append(tmpArr[k])  
                        if(len(tmpArr)==1):
                            self.rezDataFormat[i].append("")  
                            self.rezDataFormat[i].append("")   
                        if(len(tmpArr)==2):
                            self.rezDataFormat[i].append("")    
                    else:
                        self.errStr = i
                        return False                          
                else:
                    self.rezDataFormat[i].append(self.dataFormat[i][j])  
            if(len(self.rezDataFormat[i])!=13):
                self.errStr = i
                return False 
        return True      


    def get_marka_name(self, marka):
        key = unicode(marka.replace(' ','')).upper()
        # '''if(key=='1КП'):
        #     key='1'
        # if(key=='3СП'):
        #     key='3'
        # if(key=='3ГСП'):
        #     key='3'
        # if(key=='2СП'):
        #     key='2'
        # if(key=='08П'):
        #     key='08'
        # if(key=='17Г1СУ'):
        #     key='17Г1С'
        # if(key=='10Г2А'):
        #     key='10Г2'''
        # if(key=='5.0'):
        #     key = key[0:1]
        #     key='0'+key+'КП'
        # if(key=='5ПС' or key=='3ПС'):
        #     key = 'СТ'+key
        # if(key=='1ПС'):
        #     key = 'СТ'+key
        #
        # if(key=='08Х17Н6М2Т'):
        #     key = key[0:7]+key[9:10]
        # if(key=='ШХ15В'):
        #     key = key[0:4]
        # if(key=='20.0'):
        #     key='20'
        # if(key=='25.0'):
        #     key='25'
        # if(key=='10.0'):
        #     key='10'
        # if(key=='15.0'):
        #     key='15'
        # if(key=='45.0'):
        #     key='45'
        # if(key=='30.0'):
        #     key='30'
        # if(key=='35.0'):
        #     key='35'
        # if(key=='40.0'):
        #     key='40'
        # if(key=='СТАЛЬ55'):
        #     key=key[5:7]
        # if(key=='50.0'):
        #     key='50'
        # if(key=='60.0'):
        #     key='60'
        # if(key=='65.0'):
        #     key='65'
        # if(key=='70.0'):
        #     key='70'
        # '''if(key=='09Г2С-12'):
        #     key=key[0:5]
        # if(key=='Р6М5К6'):
        #     key=key[0:5]+'5'
        #
        # if(key=='4Х4ВМФС(ДИ--22)'):
        #     key=key[0:7]
        # if(key=='38Х2Н2МФА'):
        #     key=key[0:7]+key[8:9]
        # if(key=='10Х2М1ФБ'):
        #     key=key[0:6]'''
        # if(key=='0.0' or key=='0'):
        #     key = key[0:1]
        #     key='СТ'+key
        return key

    def get_gost_name(self, gost, i):
        gost_5 = ""
        rez = True
        if not gost=="":
            key=gost.replace(' ','')
            try:
                gost_5 = self.dictGost[key]
            except:
                try:
                    gost_5 = self.dictGost["ГОСТ"+key]
                except:
                    try:
                        gost_5 = self.dictGost["ГОСТР"+key]
                    except:
                        try:
                            gost_5 = self.dictGost["ГОСТ"+key+'-78']
                        except:
                            try:
                                gost_5 = self.dictGost["ГОСТ"+key+'-87']
                            except:
                                try:
                                    gost_5 = self.dictGost["ТУ"+key]
                                except:
                                    print (str(i)+" строка: Отсутствует ГОСТ,ТУ: "+key).encode('cp1251')
                                    rez=False
            if not rez:
                if((key in self.gostList) == False):
                    self.gostList.append(key)
                return False
        return gost_5


    "Форматирование загруженных данных в соответствии с указанным типом"
    def formatType(self,flag_marka):
        self.dataFormat = []
        self.dataFormatCategory = []
        # key = self.dataLoad[1][0]
        rez = True

        ErrMarka = []
        ErrMarkaCategory = []
        self.gostList = []
        markaList=[]

        indInsert=0
        # for i in range(1,3):#len(self.dataLoad)):
        for i in range(1,len(self.dataLoad)):
            # COLUMN_ID = 0
            # COLUMN_ORDER = 1
            # COLUMN_NAME = 2
            # COLUMN_SIZE_A = 3
            # COLUMN_SIZE_B = 4
            # COLUMN_SIZE_C = 5
            # COLUMN_SIZE_D = 6
            # COLUMN_SIZE_E = 7
            # COLUMN_SIZE_F = 8
            # COLUMN_SIZE_L = 9
            # COLUMN_MARKA = 10
            # COLUMN_GOST = 11
            # COLUMN_AVAILABLE = 12
            # COLUMN_PRICE = 13
            # COLUMN_ED_IZM = 14
            # COLUMN_IMAGE_1 = 15
            # COLUMN_IMAGE_2 = 16
            # COLUMN_DESCRIPTION = 17
            # COLUMN_VENDOR = 18
            # COLUMN_COUNTRY_VENDOR = 19
            # COLUMN_METHOD = 20
            # COLUMN_CATEGORY_ID = 21
            # COLUMN_SERTIFICATE_ID = 22
            # COLUMN_PRODUCT_1_ID = 23
            # COLUMN_PRODUCT_2_ID = 24
            # COLUMN_PRODUCT_3_ID = 25
            # COLUMN_PRODUCT_4_ID = 26
            # COLUMN_USLUGA_1_ID = 27
            # COLUMN_USLUGA_2_ID = 28
            # COLUMN_USLUGA_3_ID = 29
            # COLUMN_USLUGA_4_ID = 30
            self.dataFormat.append([])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_ID].replace(".0",""))
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_ORDER][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_NAME])

            #Тип металла
            category_id=""
            tmp_category_id=""
            try:
                tmp_category_id = self.dataLoad[i][COLUMN_CATEGORY_ID][:-2]
                category_id = self.dictType[int(tmp_category_id)]
            except:
                print (str(i)+" строка: Отсутствует категория с идентификатором: "+tmp_category_id).encode('cp1251')
                rez=False
                self.errStr = i
                category_id=""

            #Сохранение уникальных импортируемых категорий для дальнейшего формирования параметров
            if not (category_id in self.dataFormatCategory):
                self.dataFormatCategory.append(category_id)

            self.dataFormat[i-1].append(category_id)

            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_A])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_B])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_C])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_D])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_E])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_F])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SIZE_L])

            marka_name = self.get_marka_name(self.dataLoad[i][COLUMN_MARKA])
            # if flag_marka:
            #     marka_name = self.dataLoad[i][COLUMN_MARKA]
            if marka_name:
                marka_id=''
                try:
                    #print marka_name
                    marka_id = self.dictMarka[marka_name]
                    self.dataFormat[i-1].append(marka_id)
                except:
                    print (str(i)+" строка: Отсутствует марка: "+marka_name).encode('cp1251')
                    rez=False
                    self.errStr = i
                    if(not marka_name in ErrMarka):
                        print marka_name

                        ErrMarka.append(marka_name)
                        ErrMarkaCategory.append(self.dataLoad[i][COLUMN_DESCRIPTION])
                    self.dataFormat[i-1].append('')
            else:
                self.dataFormat[i-1].append(marka_name)

            if self.dataLoad[i][COLUMN_GOST]:
                gost_id = self.get_gost_name(self.dataLoad[i][COLUMN_GOST],i)
                if gost_id:
                    self.dataFormat[i-1].append(gost_id)
                else:
                    print (str(i)+" строка: Отсутствует ГОСТ (осн): "+self.dataLoad[i][COLUMN_GOST]).encode('cp1251')
                    rez=False
                    self.errStr = i
            else:
                self.dataFormat[i-1].append('')

            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_AVAILABLE])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_PRICE])
            if not self.dataLoad[i][COLUMN_PRICE]:
                print (str(i)+" строка: Отсутствует цена!").encode('cp1251')
                rez=False
                self.errStr = i

            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_ED_IZM])


            self.image_name_1 = ""
            self.image_name_1_http = self.dataLoad[i][COLUMN_IMAGE_1]
            self.image_name_2 = ""
            self.image_name_2_http = self.dataLoad[i][COLUMN_IMAGE_2]
            if self.dataLoad[i][COLUMN_IMAGE_1]:
                rx = re.compile('[\/]+')
                rezImg = re.split(rx,self.dataLoad[i][COLUMN_IMAGE_1])
                if rezImg[-1]:
                    self.image_name_1 = rezImg[-1]
                elif rezImg[-2]:
                    self.image_name_1 = rezImg[-2]

            if self.dataLoad[i][COLUMN_IMAGE_2]:
                rx = re.compile('[\/]+')
                rezImg = re.split(rx,self.dataLoad[i][COLUMN_IMAGE_2])
                if rezImg[-1]:
                    self.image_name_2 = rezImg[-1]
                elif rezImg[-2]:
                    self.image_name_2 = rezImg[-2]

            image_name_bd = "uploads/images/load/"+self.image_name_1
            self.dataFormat[i-1].append(image_name_bd)
            image_name_bd = "uploads/images/load/"+self.image_name_2
            self.dataFormat[i-1].append(image_name_bd)

            # import re
            # import requests
            #
            # image_name = ""
            # if self.dataLoad[i][COLUMN_IMAGE_1]:
            #     rx = re.compile('[\/]+')
            #     rez = re.split(rx,self.dataLoad[i][COLUMN_IMAGE_1])
            #
            #     if rez[-1]:
            #         image_name = rez[-1]
            #     elif rez[-2]:
            #         image_name = rez[-2]
            #     if image_name:
            #         r = requests.get('http://'+self.server+'/import_image/'+image_name+'/'+self.dataLoad[i][COLUMN_IMAGE_1])
            #         image_name = "uploads/images/load/"+image_name
            #     # print r.status_code
            # self.dataFormat[i-1].append(image_name)
            #
            # image_name = ""
            # if self.dataLoad[i][COLUMN_IMAGE_2]:
            #     rx = re.compile('[\/]+')
            #     rez = re.split(rx,self.dataLoad[i][COLUMN_IMAGE_2])
            #
            #     if rez[-1]:
            #         image_name = rez[-1]
            #     elif rez[-2]:
            #         image_name = rez[-2]
            #     if image_name:
            #         r = requests.get('http://'+self.server+'/import_image/'+image_name+'/'+self.dataLoad[i][COLUMN_IMAGE_2])
            #         image_name = "uploads/images/load/"+image_name
            #     # print r.status_code
            # self.dataFormat[i-1].append(image_name)
            #

            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_DESCRIPTION])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_VENDOR])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_COUNTRY_VENDOR])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_METHOD])


            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_SERTIFICATE_ID][:-2])


            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_PRODUCT_1_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_PRODUCT_2_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_PRODUCT_3_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_PRODUCT_4_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_USLUGA_1_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_USLUGA_2_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_USLUGA_3_ID][:-2])
            self.dataFormat[i-1].append(self.dataLoad[i][COLUMN_USLUGA_4_ID][:-2])


            self.dataFormat[i-1].append(self.image_name_1)
            self.dataFormat[i-1].append(self.image_name_2)
            self.dataFormat[i-1].append(self.image_name_1_http)
            self.dataFormat[i-1].append(self.image_name_2_http)


            #----------------


            #self.dataFormat[i].append()
            self.model2 = Qt.QSqlQueryModel(self)

            #print tmpInsert



            if(len(self.dataFormat[indInsert-1])!=8):
                self.errStr = i
                #return False
        if(not rez):

            self.dictMarkaCategory = {}
            if flag_marka:
                self.model.setTable("Marochnik_metallgroup")
                self.model.select()
                for i in range(self.model.rowCount()):
                    #print self.model.record(i).value(3).toString()
                    key = unicode(self.model.record(i).value(3).toString().replace(' ','')).upper()
                    value = self.model.record(i).value(0).toInt()[0]
                    self.dictMarkaCategory[key] = value

            print ("--- Отсутствующие марки:").encode('cp1251')
            ind_marka = 0
            for item in ErrMarka:
                print (item).encode('cp1251')
                # if(SET_PARAMETRS):


                if flag_marka:

                    self.model2 = Qt.QSqlQueryModel(self)
                    try:
                        tmpInsert = ("INSERT INTO  Marochnik_markametall (position_id,name) VALUES ('"+str(self.dictMarkaCategory[unicode(ErrMarkaCategory[ind_marka].replace(' ','')).upper()])+"','"+str(item)+"')")
                        try:
                            print tmpInsert.encode('cp1251')
                        except:
                            pass
                        self.model2.setQuery(tmpInsert)
                    except:
                        print ("--- Отсутствует категория: "+item).encode('cp1251')
                        self.errMarkaFlag = True
                    ind_marka += 1




        # if(not rez):
        #     return rez
        # if(SET_PARAMETRS):
        #     print ("Marka")
        #     for item in markaList:
        #         print (item)
        #         tmpInsert = ("INSERT INTO  categoryMetall_and_MarkaMetall  (categorymetall_id,markametall_id) VALUES ('"+
        #                          str(type_1)+"','"+
        #                          str(item)+"')")
        #         self.model2.setQuery(tmpInsert)
        #
        #     print ("GOST")
            print ("--- Отсутствующие ГОСТ:").encode('cp1251')
            for item in self.gostList:
                print (item).encode('cp1251')
                # tmpInsert = ("INSERT INTO GOST_gost (position_id,number,name) VALUES ('53','"+str(item)+"','"+str(item)+"')")
                # self.model2.setQuery(tmpInsert)
        return rez



    "Выгрузка файла в базу данных"
    def setDataDB(self):
        self.import_image_list = []
        for i in range(len(self.dataFormat)):
            print (str(i)).encode('cp1251')
            self.model2 = Qt.QSqlQueryModel(self)

            tmpInsert = "SELECT * FROM menu_product WHERE id="+str(self.dataFormat[i][COLUMN_ID])

            print (tmpInsert).encode('cp1251')
            self.model2.setQuery(tmpInsert)
            test_id = self.model2.record(0).value(0).toInt()[0]
            # print "!!!! ID"
            # print self.model2.record(0).value(0).toInt()[0]
            if test_id:
                tmpInsert = "UPDATE menu_product SET "
                tmpInsert +="order_number='"+str(self.dataFormat[i][1])+"', name_main='"+str(self.dataFormat[i][2])+"', catalog_id='"+str(self.dataFormat[i][3])+"'"
                tmpInsert +=", size_a='"+str(self.dataFormat[i][4])+"', size_b='"+str(self.dataFormat[i][5])+"', size_c='"+str(self.dataFormat[i][6])+"', size_d='"+str(self.dataFormat[i][7])+"', size_e='"+str(self.dataFormat[i][8])+"'"
                tmpInsert +=", size_f='"+str(self.dataFormat[i][9])+"', size_l='"+str(self.dataFormat[i][10])+"'"
                if self.dataFormat[i][11]=="":
                    tmpInsert +=", marka_id=NULL"
                else:
                    tmpInsert +=", marka_id='"+str(self.dataFormat[i][11])+"'"
                if self.dataFormat[i][12]=="":
                    tmpInsert +=", gost_id=NULL"
                else:
                    tmpInsert +=", gost_id='"+str(self.dataFormat[i][12])+"'"

                tmpInsert +=", available='"+str(self.dataFormat[i][13])+"', price='"+str(self.dataFormat[i][14])+"', ed_izm='"+str(self.dataFormat[i][15])+"', image='"+str(self.dataFormat[i][16])+"', image_dop='"+str(self.dataFormat[i][17])+"'"
                tmpInsert +=", description='"+str(self.dataFormat[i][18])+"', vendor='"+str(self.dataFormat[i][19])+"', vendor_country='"+str(self.dataFormat[i][20])+"'"
                tmpInsert +=", method_of_manufacture='"+str(self.dataFormat[i][21])+"'"
                if self.dataFormat[i][22]=="":
                    tmpInsert +=", sertificate_id=NULL"
                else:
                    tmpInsert +=", sertificate_id='"+str(self.dataFormat[i][22])+"'"
                tmpInsert +=" WHERE id="+self.dataFormat[i][0]
            else:
                tmpInsert = ("INSERT INTO menu_product(id, order_number, name_main, catalog_id, "
                             "size_a, size_b, size_c, size_d, size_e, size_f, size_l, marka_id, gost_id, "
                             "available, price, ed_izm, image, image_dop, description, vendor, vendor_country, "
                             "method_of_manufacture, sertificate_id) VALUES (")

                for j in range(COLUMN_SERTIFICATE_ID+1):
                    if j == 0:
                        tmpInsert+=str(self.dataFormat[i][0])

                    elif (j==11 or j==12 or j==22) and self.dataFormat[i][j]=="":
                        tmpInsert+=",NULL"
                    else:
                        tmpInsert+=",'"+str(self.dataFormat[i][j])+"'"
                tmpInsert+=")"

            try:
                print (tmpInsert).encode('cp1251')
            except:
                pass
            self.model2.setQuery(tmpInsert)




            # self.model2.setQuery(tmpInsert)
            # import time
            # time.sleep(0.5)
            import requests
            r = requests.get('http://'+self.server+'/set_slug/'+self.dataFormat[i][0]+"/"+CONTROL_CODE)
            if r.status_code != 200:
                    print "Позиция №"+str(i+1)+": Ошибка установки ссылки на страницу товара. Подозревается отсутствие товар с id="+self.dataFormat[i][0]+". В случае наличие в БД товара с данным id обратитесь к разработчику системы.".encode('cp1251')


            if self.dataFormat[i][COLUMN_IMAGE_1_TECH_NAME]:
                if not self.dataFormat[i][COLUMN_IMAGE_1_TECH_NAME] in self.import_image_list:
                    r = requests.get('http://'+self.server+'/import_image/'+self.dataFormat[i][COLUMN_IMAGE_1_TECH_NAME]+"/"+CONTROL_CODE+'/'+self.dataFormat[i][COLUMN_IMAGE_1_HTTP])
                    print 'http://'+self.server+'/import_image/'+self.dataFormat[i][COLUMN_IMAGE_1_TECH_NAME]+"/"+CONTROL_CODE+'/'+self.dataFormat[i][COLUMN_IMAGE_1_HTTP].encode('cp1251')
                    # print r.status_code
                    if r.status_code != 200:
                        print "Позиция №"+str(i+1)+": Ошибка загрузки фотографии 1 ("+self.dataFormat[i][COLUMN_IMAGE_1_HTTP]+")".encode('cp1251')
                    self.import_image_list.append(self.dataFormat[i][COLUMN_IMAGE_1_TECH_NAME])

            if self.dataFormat[i][COLUMN_IMAGE_2_TECH_NAME]:
                if not self.dataFormat[i][COLUMN_IMAGE_2_TECH_NAME] in self.import_image_list:
                    r = requests.get('http://'+self.server+'/import_image/'+self.dataFormat[i][COLUMN_IMAGE_2_TECH_NAME]+"/"+CONTROL_CODE+'/'+self.dataFormat[i][COLUMN_IMAGE_2_HTTP])
                    if r.status_code != 200:
                        print "Позиция №"+str(i+1)+": Ошибка загрузки фотографии 2 ("+self.dataFormat[i][COLUMN_IMAGE_2_HTTP]+")".encode('cp1251')
                self.import_image_list.append(self.dataFormat[i][COLUMN_IMAGE_2_TECH_NAME])
        #print str(i)

        for item in self.dataFormatCategory:
            r = requests.get('http://'+self.server+'/set_param/'+str(item)+"/"+CONTROL_CODE+'/')
            print "Формирование параметров категории (id="+str(item)+")".encode('cp1251')
            if r.status_code != 200:
                print "Ошибка формирования параметров категории (id="+str(item)+")".encode('cp1251')

        
        '''self.model.select()
        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                print(self.model.record(i).value(j).toString())
            print("")'''
    def clearDB(self):
        Answer = QtGui.QMessageBox(QtGui.QMessageBox.Warning,\
                "Система ввода продукции","Вы действительно хотите загрузить новые марки в базу данных продукции?",\
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No ).exec_()

        if Answer == QtGui.QMessageBox.No:
            #Отказались от очистки БД
            return
        self.importDB(True)

        # self.model.setTable("catalog")
        # self.model.select()
        # self.model.removeRows(0, self.model.rowCount())
        # self.model.submitAll()
        # self.model.setTable("lastNumber")
        # self.model.select()
        # self.model.setData(self.model.index(0, 0),0 )
        # self.model.submitAll()
        if not self.errMarkaFlag:
            self.showMessageInfo('Новые марки в базу данных продукции успешно загружены!')
        else:
            self.showMessageError('ОШИБКА! загрузки марок')

        
    def clearDataLoadNumber(self):
        tmpNum = self.spinBoxNumber.value()
        Answer = QtGui.QMessageBox(QtGui.QMessageBox.Warning,\
                "Система ввода продукции","Вы действительно хотите удалить данные загрузки № "+str(tmpNum)+"?",\
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No ).exec_()

        if Answer == QtGui.QMessageBox.No:
            #Отказались от очистки БД
            return
        
        self.model.setTable("catalog")
        self.model.setFilter("flagNumber='"+str(tmpNum)+"'")
        self.model.select() 
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.showMessageInfo('Данные загрузки № '+str(tmpNum)+' из базы данных продукции успешно удалены!')
        
    def showMessageInfo(self,strMsg):
        QtGui.QMessageBox(QtGui.QMessageBox.Information,\
                "Система ввода продукции",strMsg,\
                QtGui.QMessageBox.Ok ).exec_()
                
    def showMessageError(self,strMsg):
        QtGui.QMessageBox(QtGui.QMessageBox.Critical,\
                "Система ввода продукции",strMsg,\
                QtGui.QMessageBox.Ok ).exec_()

            
            
app = QtGui.QApplication(sys.argv)  # создаёт основной объект программы
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("UTF-8"))
QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("UTF-8"))
QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("UTF-8"))

MainWindow = MainWindow() 
if(MainWindow.errConnect == True):
    exit()
MainWindow.show()
app.exec_()
