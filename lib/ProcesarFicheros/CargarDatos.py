# -*- coding: utf-8 -*-


import os

"""Modulo que se encarga de cargar las estructuras de datos del proyecto *MITAD*.
   @author: Saul Blanco Fortes
   @contact: saul.blanco@bluethinking.com
   @version: 1.0
"""




class Palabra:
	"""Esta clase contiene los datos que guardamos de una palabra, su peso y la palabra en si. Además de acceso a los mismos:"""
	__palabra = ''
	__peso	  = 0

	def __init__ ( self, palabra, peso ):
		self.__palabra 	= palabra
		self.__peso	= peso

	def getPalabra ( self ):
		return self.__palabra

	def getPeso ( self ):
		return self.__peso


class manejarUTF:
	"""Esta clase filtra los caracteres extrannos para que Python pueda hacer bien las comparaciones de cadena:"""
	__charsToConvert	= {'á':'-a-','é':'-e-','í':'-i-','ó':'-o-','ú':'-u-',',':' ','.':'','?':'','¿':'','!':'','¡':'','ñ':'-n-','ü':'','//':'','\\':'','(':'',')':'','»':'','«':'','/':'_',':':''}
	__charsInverso		= {}
	__palabras			= []
	__texto				= []
	__textonltk			= ""
	__frecPalabras		= {}



	def __init__ ( self ):
		#Construimos el inverso de los caracteres para poder decodificar el texto:
		for k in self.__charsToConvert.keys():
			if ( self.__charsToConvert [ k]  ):
				self.__charsInverso [ self.__charsToConvert [ k] ] = k
		del ( self.__charsInverso [' '] )


	def imprimirTodo ( self ):
		for k in self.__charsToConvert.keys():
			print "%s -> %s" % ( k, self.__charsToConvert[k] )

		for k in self.__charsInverso.keys():
			print "%s -> %s" % ( k, self.__charsInverso[k] )



	def codificarTexto ( self, txt ):
	
		keylist = self.__charsToConvert.keys()
		keylist.sort()
		for key in keylist:
			txt = txt.replace ( key, self.__charsToConvert[ key] )
		return txt

	def decodificarTexto ( self, txt ):

		for key in self.__charsInverso.keys():
			txt = txt.replace ( key, self.__charsInverso[ key] )
		return txt





class ResumenDirectorio:
	"""En la claes CargarDirectorio se encuentra toda la estructura de ficheros palabras y pesos para una comparacion dada. En esta clase se guarda un resumen que guarda, para cada comparacion (frec, sem, manual..), el nombre del fichero y las coincidencias encontradas"""

	__resumen	= {}

	def __init__ (self  ):
		self.__resumen	= {}

	def addFichero ( self, nombreFich, numCoincidencias ):
		self.__resumen [nombreFich] = numCoincidencias

	def getListFiles ( self ):
		"""Devuelve la lista de ficheros de un directorio concreto."""
		lista	= self.__resumen.keys ()
		lista.sort ()
		return lista

	def getCoinci ( self, fich ):
		return self.__resumen [fich] 




class CargarDirectorio:

	"""Aqui es donde guardamos el contenido de un directorio (sem, frec, manual..) Se carga el contenido de cada fichero, y por cada fichero las palabras que contienen y su peso (de tenerlo)"""

	__descripcion	= '' 


	def __init__ (self, directorio, descripcion ):
		'''
		Constructor: recibe el directorio a recorrer y una descripcion textual, y carga el contenido cada palabra del fichero en un diccionario [fichero] -> [listapalabras] -> (palabra,peso)
		'''

		print "procesando directorio %s" % ( directorio )

		self.__descripcion = descripcion

		m = manejarUTF ()
		self.__fichero	= {}
		for root, dirs, files in os.walk( directorio ):
			for file in [f for f in files]:
				listaPalabras = []

				for x in open ( os.path.join(root, file), "r").readlines ():
					x = x.strip ()
					x = x.replace ( '\n', '' )
					#Este simoblo aparece en algunos de los ficheros, desconocemos el motivo :(
					x = x.replace ('\xef\xbb\xbf','')

					#Si estan separados por : es palabra : peso
					if x.find (':') != -1:
						lista 	= x.split (':')
						listaPalabras.append ( Palabra ( m.codificarTexto ( lista[0].strip() ).lower(), lista[1].strip () ))
					#Si es una coma entonces son varias palabras separadas por comas palabra1, palabra2 etc
					elif x.find (',') != -1:
						lista 	= x.split (',')
						for l in lista:
							print 'Encontrada una coma %s en %s' % ( l,  os.path.join(root, file) )
							listaPalabras.append ( Palabra ( m.codificarTexto ( l.strip() ).lower(), 0 ) )
					#Si no es nada de lo anterior, entonces es una palabra monda y lironda, de infanteria.
					else:
						listaPalabras.append ( Palabra ( m.codificarTexto ( x ).lower(),0 ) )

				nombref	= file.split ('.')
				self.__fichero [ int (nombref[0]) ] = listaPalabras



					

	def printFile ( self, fichero ):
		"""Se le pasa un fichero como parametro, lo busca en el diccionario, e imprime la lista de cada palabra con su peso correspondiente."""
		lista = self.__fichero[ fichero ]

		for palabra in lista:
			print '{%s} -> {%s}' % ( palabra.getPalabra () , palabra.getPeso () )

	def getListFiles ( self ):
		"""Devuelve la lista de ficheros de un directorio concreto."""
		lista = self.__fichero.keys ()
		lista.sort()
		return lista
			
	def getDescripcion ( self ):
		"""Devuelve la descripcion textual que se puso al directorio al crearlo."""
		return self.__descripcion


	def getPalabras ( self, fichero ):
		"""Devuelve la lista de palabras que contiene un fichero, Cada palabra es una tupla (palabra, peso)"""
		return self.__fichero [ fichero ]


	def getPesoPalabra (self, fichero, palabra ):
		"""Devuelve el peso de una palabra concreta en un fichero concreto. En caso de no encontrarla, devuelve un -1"""
		
		for p in self.__fichero [ fichero ]:
			if p.getPalabra () == palabra:
				return p.getPeso ()

		return -1







