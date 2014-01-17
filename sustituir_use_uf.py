# -*- coding: latin-1 -*-

from   lib.ProcesarFicheros.CargarDatos import *
import argparse
import os
import csv


#cargamos la correspondencia uf / use desde el fichero pasado como parametro.
def cargarSustituciones ( fich ):
	sustituciones = {}
	mUTF8		  = manejarUTF ()

	lineas = csv.reader(open( fich ),delimiter=',')
	for line in lineas:
		uf  = (mUTF8.codificarTexto ( line[1].strip () )).lower()
		use = (mUTF8.codificarTexto ( line[0].strip () )).lower()

		sustituciones [uf] = use

		#print ("Cambiar -%s- por  -%s-") % ( uf, use )

	return sustituciones




def ensure_dir(f):
	d = os.path.dirname(f)

	if not os.path.exists(d):
		os.makedirs(d)

#######################################
#######################################
#######################################
#######################################

#python sustituir_use_uf.py use_uf/USE-UF.csv use_uf/EliminarNoPreferentes/ use_uf/SalidaFicheros/ txt

#######################################
#######################################
#######################################
#######################################


if __name__ == "__main__":

	parser	= argparse.ArgumentParser ( description='Recibe un CSV con dos columnas, use y uf, y sustituye todos las ocurrencias en todos los ficheros del directorio indicado de las palabras en uf por las de use' )

	parser.add_argument('ficherouseuf'  , action = "store", metavar='fichero', type=str, help='Fichero use uf')
	parser.add_argument('directorio'  , action = "store", metavar='dir', type=str, help='Directorio con los ficheros a sustituir')
	parser.add_argument('directoriosalida'  , action = "store", metavar='dirsalida', type=str, help='Directorio con los ficheros a sustituir')
	parser.add_argument('extension'  , action = "store", metavar='ext', type=str, help='Extension de esos ficheros')

	args 			= parser.parse_args()

	sustituciones 	= cargarSustituciones ( args.ficherouseuf )
	mUTF8			= manejarUTF ()

	for root,dirs,files in os.walk( args.directorio ):
		for file in [f for f in files if f.lower().endswith( 'txt' )]:

			nombre 			= file
			nombredestino	= args.directoriosalida + '/'+ root + '/' + nombre

			#Creamos el directorio si hace falta:
			ensure_dir ( nombredestino )

			f = open(nombredestino,'w')


			for x in open ( os.path.join(root, file), "r").readlines ():
				cadena_final = x.replace ('\n','')
				lista	     = x.split (':')
				x	     = lista [0].strip ().lower()
				peso	     = lista [1].replace ('\n','')

				cad =  mUTF8.codificarTexto ( x ) 
				
				for key in sustituciones.keys ():
					if cad == key:
						print "He reemplazado -%s- por -%s- en el fichero %s/%s" % ( mUTF8.decodificarTexto ( cad), mUTF8.decodificarTexto ( sustituciones[key]),root, nombre)
						cadena_final = mUTF8.decodificarTexto ( sustituciones[key]) + ':' + peso


				f.write( cadena_final + '\n') # python will convert \n to os.linesep

			f.close ()
















