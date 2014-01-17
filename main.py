# -*- coding: latin-1 -*-

from   lib.ProcesarFicheros.CargarDatos import *
from   lib.ProcesarFicheros.HojaCalculo import *



import argparse
import os



#python main.py DocumentosPrueba/Manual/ DocumentosPrueba/Frec Documentos/FrecSem/ Documentos/Sem/ Salida/ --compara 5 --compara 10

def comparar ( origen, destino, num, salida ):


	resumen = {}

	print "Comparando %s con %s" % ( origen.getDescripcion (), destino.getDescripcion () )


	#Creamos una hoja de calc cuyo nomgre sera el origen y el destino frec_sem manual_frec etc
	wb		= Workbook ()
	ficherohc	= CrearHojaCalc ( wb )

	#Filas en la que escribir, una para cada hoja. Guardamos una para cada hoja. Las diferentes hojas seran el numero de comparaciones solicitadas (10,15,20..)
	posY 		= {}

	#Las ponemos a cero:
	for n in num:
		#Una hoja nueva en cada fichero con el numero (5,10,15)
		ficherohc.addSheet ( str ( n ) )
		#Se guarda un total con los resultados:
		resumen[int(n)]	= ResumenDirectorio ( )
		posY[n]		= 0


	mUTF8	= manejarUTF ()

	#Por cada fichero del directorio origen:
	for f in origen.getListFiles ():

		#Se compara el que tenga mas palabras con el que tiene menos:
		palOr	= origen.getPalabras  ( f )
		palDest	= destino.getPalabras ( f )

		if len ( palOr) < len (palDest ):
			#print "Comparando %s con %s" % ( destino.getDescripcion (), origen.getDescripcion () )
			#print "cambiando origen / destino"
			palOr	= destino.getPalabras ( f )
			palDest	= origen.getPalabras (f)

		#Sacamos la lista de palabras, sin su peso asociado, solo la palabra:
		palDestNombres = []
		for p in palDest:
			palDestNombres.append ( p.getPalabra () )

		palDestNombres = palDestNombres [ : (int(n)) ]
		#Y comparamos para cada n (10,15,20...)
		for n in num:
			palOrTmp 		  = palOr [: (int (n)) ]
			palDestNombresTmp = palDestNombres [ : (int(n)) ]
			#print "Comparando para %s" % ( n )
			coincidencias	= []
			for p in palOrTmp:
				if p.getPalabra () in palDestNombresTmp:
					coincidencias.append ( p )
					print ('Encontrada coincidencia %s en %s para %s / %s_%s') % (p.getPalabra(), f, n, origen.getDescripcion (), destino.getDescripcion () )

			posX = 0

			#Al grabar en el fichero debemos hacerlo posicionando el texto en una fila y una columna. Debemos guardar esos datos para las siguientes pasadas:

			if len (coincidencias) > 0:
				ficherohc.grabarDato (str (n), posX,posY[n], f )
				posX	+= 1
				ficherohc.grabarDato (str (n), posX,posY[n], int ( len (coincidencias) ) )
				posX	+= 1
				resumen[int (n)].addFichero ( f, int ( len (coincidencias) ) )
			else:
				resumen[int (n)].addFichero ( f, 0 )

			for c in coincidencias:
				ficherohc.grabarDato (str (n), posX,posY[n], mUTF8.decodificarTexto ( c.getPalabra () ) )
				posX	+= 1
				ficherohc.grabarDato (str (n), posX,posY[n], int ( c.getPeso () ))
				posX	+= 1
				pesoDest = destino.getPesoPalabra (f, c.getPalabra() )
				ficherohc.grabarDato (str (n), posX,posY[n], int (pesoDest) )
				posX	+= 1

			if len (coincidencias) > 0 : 
				posY[n] += 1
				


	wb.save (salida + '/' + origen.getDescripcion () + '_' + destino.getDescripcion () + '.xls')
	return resumen






def guardarResumen ( R, listaHojas, salida ):

	wb		= Workbook ()
	ficherohc	= CrearHojaCalc ( wb )


	for l in listaHojas:
		ficherohc.addSheet ( str ( l ) )


	#Creamos la linea de titulos de cada hoja donde figura el tipo de comparacion frec, frec_sem:
	posY = 0
	listaResu = []


	for hoja in listaHojas:
		posX = 1
		for idresumen in  sorted(R.keys ()):
			ficherohc.grabarDato ( str (hoja), posX, posY, idresumen )
			posX = posX + 1
			if not (idresumen in listaResu):
				listaResu.append ( idresumen )

	posX = 0

	#Grabamos los nombres de los ficheros ordenados en la columna 1
	listaFicheros	=  R [idresumen][int(hoja)].getListFiles () 

	for hoja in listaHojas:
		posY = 1
		for f in listaFicheros:
			ficherohc.grabarDato (str (hoja), posX,posY, f )
			posY = posY + 1


	#Ahora grabamos para cada una de las filas y columnas rellenadas antes, los valores reales:
	for hoja in listaHojas:
		posX = 1
		for resactual in listaResu:
			posY = 1
			for f in listaFicheros:
				ficherohc.grabarDato (str (hoja), posX,posY, R[resactual][int(hoja)].getCoinci ( f ) )
				posY = posY + 1
			posX = posX + 1






	wb.save (salida + '/' + 'ResumenTotal.xls')



		

	



if __name__ == "__main__":

	FicherosTotal	= {}
	ResumenTotal	= {}

	parser	= argparse.ArgumentParser ( description='Recibe un directorio de entrada y lo recorre (incluyendo los subdirectorios) buscando y contabilizando la existencia de las palabras pasadas como parametro en otro fichero .' )

	parser.add_argument('manual'  , action = "store", metavar='dirmanual', type=str, help='Directorio con los ficheros manual')
	parser.add_argument('frec' , action = "store", metavar='dirfrec',   type=str, help='Directorio con los ficheros frec')
	parser.add_argument('frecsem' , action = "store", metavar='dirfrecsem',   type=str, help='Directorio con los ficheros frecsem')
	parser.add_argument('sem' , action = "store", metavar='dirsem',   type=str, help='Directorio con los ficheros sem')
	parser.add_argument('salida' , action = "store", metavar='salida',   type=str, help='Directorio donde volcar los datos')
	parser.add_argument('--compara', action = "append", metavar='itemscomparar', help='numero de items a comparar.')


	args 	= parser.parse_args()

	FicherosTotal['manual'] = CargarDirectorio ( args.manual, 'manual' )
	FicherosTotal['frec'] = CargarDirectorio ( args.frec, 'frec' )
	FicherosTotal['frecsem'] = CargarDirectorio ( args.frecsem, 'frecsem' )
	FicherosTotal['sem'] = CargarDirectorio ( args.sem, 'sem' )


	#FicherosTotal['manual'].printFile ( 37 )

	#En este punto tenemos cada directorio (manual, frec...) junto con el contenido de cada fichero, contenido en memoria.
	#Pasamos a realizar las comparaciones entre cada directorio:

	ResumenTotal ['manual_frec']		= comparar ( FicherosTotal['manual'], FicherosTotal['frec'], args.compara, args.salida )
	ResumenTotal ['manual_sem']			= comparar ( FicherosTotal['manual'], FicherosTotal['sem'], args.compara, args.salida )
	ResumenTotal ['manual_frecsem']		= comparar ( FicherosTotal['manual'], FicherosTotal['frecsem'], args.compara, args.salida )
	ResumenTotal ['frec_sem']		= comparar ( FicherosTotal['frec'], FicherosTotal['sem'], args.compara, args.salida )
	ResumenTotal ['frec_frecsem']		= comparar ( FicherosTotal['frec'], FicherosTotal['frecsem'], args.compara, args.salida )
	ResumenTotal ['frecsem_sem']		= comparar ( FicherosTotal['frecsem'], FicherosTotal['sem'], args.compara, args.salida )


	guardarResumen ( ResumenTotal, args.compara, args.salida )





