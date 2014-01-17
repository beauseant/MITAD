# -*- coding: utf-8 -*-

#http://snatverk.blogspot.com.es/2011/04/generar-ficheros-excel-con-python.html



from pyExcelerator import *
import codecs


class CrearHojaCalc:

	__workbook	= Workbook()
	__sheet		= {}


	def __init__ (self, wb):
		self.__workbook = wb

	def addSheet (self, nombre, w= '0x24E1'):
		self.__sheet[nombre]	=  self.__workbook.add_sheet( unicode ( nombre, "utf8") )
		self.__sheet[nombre].col(0).width = 0x24E1

	def grabarDato (self, hoja, posy, posx, dato):
		h = self.__sheet [hoja]
		if isinstance( dato, basestring ):
			h.write (posx, posy,  unicode ( str(dato), "utf8" ) )
		else:
			h.write (posx, posy,  dato )



