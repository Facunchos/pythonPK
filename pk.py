import os
import numpy as np
import time
import sys
import subprocess
from tabulate import tabulate

#Constants
STATS = ('Fuerza','Agilidad','Fe','Entendimiento','Bravura','Personalidad')
ANE = ['ATRAS','NUEVO','EDITAR']
ABN = ['ATRAS','BORRAR','NUEVO']
ABNE = ['ATRAS','BORRAR','NUEVO','EDITAR']
ORDEN = ['MENU', 'SHOWPJS','PJ', 'EDITPJ' ]
INFO_CON_NOMBRE = {'habilidades':['Nivel', 'Stat', 'BonusTirado', 'BonusGuardado', 'Bonus', 'Descripcion'], 'hechizos':['Descripcion'], 'tecnicas':['Detalle'], 'ventajas':['Detalle']}
INFO_SIN_NOMBRE = {'notas':['Detalle'], 'notasEsp':['Detalle'],}
PATH_FOLDER = './pjs/'
S = '\n'

# https://www.geeksforgeeks.org/python-dictionary/
#All files from folder in array [], checking for pjs already created
def checkFolder():
	#Check for the folder. If exists, proceeds, else creates it with Auth from User. If user not want, cancel operation.
	if not os.path.isdir('pjs'):
		askAuthUser = input('Se ha creado la carpeta "pjs" para almacenar los personajes')
		os.makedirs('pjs')
	return os.listdir(PATH_FOLDER)
		
#Array of files names in the pjs folder
def listPJ():
	return checkFolder()

LISTPJ = listPJ() 
#If no pjs, create the first
def checkForPjs():
	#Check if the pjs folder is created. If not create one
	checkFolder()
	listPJ()
	#Show all the characters avairable
	eleccion = showPjs(ABN)
	
	if eleccion in ABN:
		opciones(eleccion, ORDEN[0], esPJ = True)
	else:
		print('Haz elejido a : ',eleccion)
		showPjInfo(eleccion)

def showPjInfo(pjName):
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	elegido = showAndChoose(claves, ANE)
	if elegido not in ABNE:
		#Shows the info of the key choosed
		print(pj[elegido], )
		if isinstance(pj[elegido], dict): showTable(pj[elegido]) 
		input()
		#And then shows all the keys again
		showPjInfo(pjName)
	else:
		#If 'ATRAS' send ORDEN
		opciones(elegido, ORDEN[1], pjName)

# not working	
def showTable(data):
	print(tabulate(data	, headers='keys', tablefmt='github'))
	

def opciones(el, orden = None, pjName = None, esPJ = False):
	print('orden', orden, 'pjName', pjName)
	if el == 'ATRAS':
		atras(orden, pjName)
	elif el == 'BORRAR':
		delPj() if esPJ else None
	elif el == 'NUEVO':
		addPj() if esPJ else askNew(pjName)
	elif el == 'EDITAR':
		editPj(pjName)
		
def atras(orden, pjName = None):
	if orden == ORDEN[0]:
		menu()
	elif orden == ORDEN[1]:
		checkForPjs()
	elif orden == ORDEN[2]:
		showPjInfo(pjName)
	elif orden == ORDEN[3]:
		showPjInfo(pjName)

def getPj(pjName):
	personaje = {}
	with open(PATH_FOLDER + pjName) as file:
		#eval() reads the file content and returns an array
		personaje = eval(file.read())

	return personaje
	
def getPjKeys(pjName):
	pj = getPj(pjName)		
	return list(pj.keys())
	
#Print a link
def link(uri, label=None):
	if label is None: 
		label = uri

	parameters = ''

	# OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
	escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

	return escape_mask.format(parameters, uri, label)

def menu():
	#Only 'Personajes' has more options, the rest is a link
	links = {'Manual': 'https://drive.google.com/drive/u/0/folders/1cLwQJNBNFOMCxDp7t_fC4DHqz9kdyJUA', 'Hoja Excel':'https://docs.google.com/spreadsheets/d/1CA0mS23IgUdEZ-WnBhtf66BKSf_Mvkb83Yp-YzjG7uQ/edit#gid=2043668604', 'Creditos': 'Creado por Facundo Martinez (Facunchos) En 2024 \n Linkedin: \n https://www.linkedin.com/in/facunmartinez/ \n GitHub: \n https://github.com/Facunchos', 'Cafesito': 'Hacerme cuenta de Cafesito!',  }
#	inicio = ['Personajes', 'Manual' ,'Hoja Excel','Creditos','Cafesito', 'Refresh', 'Refresh File names']
	
	inicio = ['Personajes', 'Manual' ,'Hoja Excel','Creditos','Cafesito', 'Refresh File names']
	elegido = showAndChoose(inicio)
	if elegido in links.keys():
		print(links[elegido])
		menu()
	elif elegido == 'Personajes':
		checkForPjs()
	elif elegido == 'Refresh':
		refresh()
	elif elegido == 'Refresh File names':
		refreshFileName()
	else:
		print('Elija una opcion correcta')
		menu()

def showAndChoose(lista, optExit = None):
	#lista = show this options (array)
	#optExit = show x- exit, like that
	print(S)
	#Join both arrays into one
	lista_table = lista
	if optExit != None:
		lista = np.concatenate((np.array(optExit), np.array(lista)))
		
	#Show the options
	options = list(range(len(lista)))  # List the valid options
	i=0   
	while i < len(lista):
		print(i,'-    ',lista[i])
		i+=1
	# Choose one ~valid~
	while True:
		statUsa = input('Elija uno: ')	

		if not statUsa.isdigit():  # Verificar si la entrada es un número
		    print('Ingrese un número válido.')
		    #The continue ejecutes the While again
		    continue
		
		statUsa = int(statUsa)
     	 	
		if statUsa not in options:
			print('Agregue una opcion valida')
			continue
		return lista[statUsa]
	

# Show all the stats, choose one and return the name
def showStats():
	return showAndChoose(STATS)
		
# Show all the characters, choose one and return the name 
def showPjs(opt = None):
	return showAndChoose(LISTPJ, opt)
	
# For adding more stuff to a PJ. Like Habilidades, Hechizos, Notas, etc. But asks USER first
def askNew(pjName):
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	delet = ['name', 'raza', 'xp']
	newlyAdded = False
	# Generate a new list containing only those elements from clave that are n present in the delet
	clave_filtered = [key for key in claves if key not in delet]

	print('Que quieres agregar?: ')
	elegido = showAndChoose(clave_filtered, ['ATRAS'])
	
	if elegido in INFO_CON_NOMBRE.keys():
		newlyAdded = addNew(INFO_CON_NOMBRE[elegido], True)
	elif elegido in INFO_SIN_NOMBRE.keys():
		newlyAdded = addNew(INFO_SIN_NOMBRE[elegido], False)
	else:
		print('No se encontro que se quiere modificar')
		
	pj[elegido].update(newlyAdded)  # Update existing habilidades with the new one
	
	if newlyAdded:
		with open(PATH_FOLDER + pjName, 'w') as file:	
			file.write(str(pj)) 
	opciones('ATRAS', ORDEN[2], pjName=pjName)   
      
# example addNew([Nombre, Nivel, Stat que usa, Bonus Tirado], True)
# Cycles the list[], asking for a value for each KEY, transforming the ARR into DICT. If the name parameter is True, ask for it.
# Name = False: (Return = {}); Name = True: (Return = Name:{})
def addNew(lista, nombre = False):

	#lista is a array of things to cicle
	res = {}
	if nombre:
		nombre = input('Ingrese un nombre: ')
		res[nombre] = {}
		res[nombre] = {i: input(f'Ingrese {i}: \n') for i in lista}
	else:
		res = {i: input(f'Ingrese {i}: \n') for i in lista}
	
	return res

def editPj(pjName):
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	while True:
		print('Que quieres modificar?')
		primer = showAndChoose(claves, ['ATRAS'])
		if primer == 'ATRAS':
			opciones(primer, ORDEN[2], pjName)
			break  # Exit the loop if user chooses 'ATRAS'

		# If not dict, edit. If dict, ask again what. You can only edit what's inside the dict, not the dict.
		if not isinstance(pj[primer], dict):
			pj[primer] = modificarString(pj[primer])
			break
		else:
			while True:
				primerList = list(pj[primer])
				for i in primerList:
				        print(i, '  ', pj[primer][i], S)
				segundo = showAndChoose(primerList)

				# Is a Dict inside a Dict? Loop again
				if not isinstance(pj[primer][segundo], dict):
				        pj[primer][segundo] = modificarString(pj[primer][segundo])
				        break
				else:
					while True:
						segunList = list(pj[primer][segundo])
						for i in segunList:
							print(i, '  ', pj[primer][segundo][i], S)
						tercer = showAndChoose(segunList)

						if not isinstance(pj[primer][segundo][tercer], dict):
							pj[primer][segundo][tercer] = modificarString(pj[primer][segundo][tercer])
							print('aca')
							break
						else:
							print("Cannot edit nested dictionaries further.")
							break  # Ask for input again if user tries to edit nested dictionaries
				break  # Exit the loop after editing the nested dictionary

	with open(PATH_FOLDER + pjName, 'w') as file:
		file.write(str(pj))

	opciones('ATRAS', ORDEN[2], pjName)

def modificarString(info):
	print('Modificando: ', info )
	nuevoInput = input('Ingrese nuevo valor: \n')
	print('Valor anterior: ', info)			  	
	print('Valor Nuevo: ', nuevoInput )
	return nuevoInput
		

def addPj():
	nombre = input('Elija el nombre del personaje: ')
	#Set Dictionaries
	personaje = {}
	stats = {}
	habilidades = {}	
	hechizos = {}
	notas = {}
	notasEsp = {}
	tecnicas = {}
	ventajas = {}
	path = PATH_FOLDER+nombre
	#opciones = ['Habilidades','Tecnicas','Stats','Inventario']
	#Create file with character name
	personaje['name'] = nombre
	print('Vamos a crear paso a paso')
	#Raza
	personaje['raza'] = input('Ingrese la raza: ')
	
	#XP
	print('Hay 2 tipos de XP, la usada y la disponible.')		
	personaje['xp'] = addNew(['usada','disponible'])
	
	#Stats
	stats = addNew(STATS)
	
	#Hechizos
	if input('Hechizo? y/any \n').lower() == 'y': hechizos = addNew(INFO_CON_NOMBRE['hechizos'], True)

	#Habilidades
	if input('Habilidad? y/any \n').lower() == 'y': habilidades = addNew(INFO_CON_NOMBRE['habilidades'], True)
	
	personaje['habilidades'] = habilidades
	personaje['hechizos'] = hechizos
	personaje['stats'] = stats
	personaje['notas'] = notas
	personaje['notasEsp'] = notasEsp
	personaje['tecnicas'] = tecnicas
	personaje['ventajas'] = ventajas
	with open(path, 'x') as file:
		file.write(str(personaje))
		print(personaje, '\n\n')
		
	checkForPjs()
			
		#Mostrar el nombre en grande del elegido junto con las opciones de Ver, Editar, Eliminar o Atras
		
#Remove Character FILE
def delPj():
	seguro = input('ESTAS SEGURO? y/any \n')
	if seguro.lower() != 'y':
		checkForPjs()
		
	print('Cual deseas BORRAR?: ')
	eleccion = showPjs(['ATRAS'])
	if eleccion in ABNE:
		opciones(eleccion, ORDEN[1])	
	else:
		path = PATH_FOLDER + eleccion
		if os.path.exists(path):
			os.remove(path)
			print('Archivo removido con exito')
		else:
			print("The file does not exist") 
	start()
		
def refreshFileName(backToMenu = True):
	pjs = os.listdir(PATH_FOLDER)
	for i in pjs:
		name = getPj(i)['name']
		if i != name:
			print(f'Nombre de archivo actualizado. De {i} a {name}')
			os.rename(PATH_FOLDER+i, PATH_FOLDER+name)
	if backToMenu: atras(ORDEN[0])

"""
	def refresh():
		# Get the command to execute the script again
		python_executable = sys.executable
		script_path = sys.argv[0]
		command = [python_executable, script_path]

		# Launch a new instance of the Python interpreter to run the script again
		subprocess.Popen(command)
		os.system("gnome-terminal --command 'python3 pk.py';bash -c 'exit' ")
		# Terminate the current script execution
		sys.exit()
"""
# Two spaces and waits till input from USER
def any():
	print(S)
	input('Press any key to continue')

def start():
	#Greetings
	print('Bienvenido a PainKiller charactermancer by Facunchos')
	any()
	menu()

start()			
