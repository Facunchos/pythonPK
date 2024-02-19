import os
import numpy as np
import time
statsTuple = ('Fuerza','Agilidad','Fe','Entendimiento','Bravura','Personalidad')
ANE = ['ATRAS','NUEVO','EDITAR']
ABN = ['ATRAS','BORRAR','NUEVO']
ABNE = ['ATRAS','BORRAR','NUEVO','EDITAR']
ORDEN = ['MENU', 'SHOWPJS','PJ', 'EDITPJ' ]

# https://www.geeksforgeeks.org/python-dictionary/
PATH_FOLDER = './pjs/'
S = '\n'
#All files from folder in array [], checking for pjs already created
def checkFolder():
	#Check for the folder. If exists, proceeds, else creates it with Auth from User. If user not want, cancel operation.
	if not os.path.isdir('pjs'):
		askAuthUser = input('Se ha creado la carpeta "pjs" para almacenar los personajes')
		os.makedirs('pjs')
	return os.listdir(PATH_FOLDER)
		
#Array of files names in the pjs folder
listPjs = checkFolder()
#If no pjs, create the first
def checkForPjs():
	#Check if the pjs folder is created. If not create one
	checkFolder()
	#Show all the characters avairable
	eleccion = showPjs(ABN)
	
	if eleccion == 'ATRAS':
		opciones(eleccion, ORDEN[0])
	elif eleccion == 'BORRAR':
		seguro = input('ESTAS SEGURO? y/any \n')
		if seguro.lower() == 'y':
			delPj()
		else:
			checkForPjs()
	elif eleccion == 'NUEVO':
		addPj()
	else:
		print('Haz elejido a : ',eleccion)
		showPjInfo(eleccion)
		
	# Hacer una funcion aparte para esto

def showPjInfo(pjName):
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	elegido = showAndChoose(claves, ANE)
	if elegido not in ABNE:
		#Shows the info of the key choosed
		print(pj[elegido], )
		time.sleep(3)
		#And then shows all the keys again
		showPjInfo(pjName)
	else:
		#If 'ATRAS' send ORDEN
		opciones(elegido, ORDEN[1], pjName)

#Falta hace el nuevo
def opciones(el, orden = None, pjName = None,):
	print('orden', orden, 'pjName', pjName)
	if el == 'ATRAS':
		atras(orden, pjName)
	elif el == 'BORRAR':
		print('')
	elif el == 'NUEVO':
		askNew(pjName)
		print('')
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
	inicio = ['Personajes', 'Manual' ,'Hoja Excel','Creditos','Cafesito', 'Refresh', 'Refresh File names']
	
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
	
	#Join both arrays into one
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
		    continue
		
		statUsa = int(statUsa)
     	 	
		if statUsa not in options:
			print('Agregue una opcion valida')
			continue
		return lista[statUsa]
	

# Show all the stats, choose one and return the name
def showStats():
	return showAndChoose(statsTuple)
		
# Show all the characters, choose one and return the name 
def showPjs(opt = None):
	return showAndChoose(listPjs, opt)

# Add hechizo
def addHechizo():
	hechizo = {}
	print('Agregando hechizo: Nombre, Descripcion ')
	nombre = input('Nombre: ')
	des = input('Agregue descripcion')
	hechizo[nombre.lower()] = des.lower()
	return hechizo;
	
def addHabilidad():
	habilidad = {}  # Inicializar la variable habilidad

	print('Agregando habilidad: Nombre, Nivel, Stat que usa, Bonus Tirado, Bonus Guardado, Bonus al total, Descripcion')
	nombre = input('Nombre: ')
	habilidad[nombre] = {}
	habilidad[nombre]['nivel'] = input('Nivel: ')

	# Show the Stats options
	habilidad[nombre]['Stat'] = showStats()

	# Add validations for integer inputs
	while True:
		try:
			habilidad[nombre]['bonusTirado'] = int(input('Bonus de dados que se tiran (BonusTirado): '))
			habilidad[nombre]['bonusGuardado'] = int(input('Bonus de dados que se guardan (BonusGuardado): '))
			habilidad[nombre]['bonus'] = int(input('Bonus que se suma a la tirada total (Bonus): '))
			break  # Break the loop if all inputs are valid integers
		except ValueError:
			print('Ingrese un número entero válido.')

	habilidad[nombre]['des'] = input('Agregue descripción: ')
	print(habilidad)
	return habilidad
	
# example addNew([Nombre, Nivel, Stat que usa, Bonus Tirado])
# Aca le mando un array de nombres que va ciclar el for. Se le pide un nombre inicial y una carga de datos
"""
def askNew(pjName, ):
	
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	delet = ['name','raza','xp']
	
	#generates a new list containing only those elements from clave that are not present in the delet
	clave_filtered = [key for key in claves if key not in delet]

	print('Que quieres agregar?: ')	
	elegido = showAndChoose(clave_filtered, ['ATRAS'])
	#opciones: ['habilidades', 'hechizos', 'stats', 'notas', 'notasEsp', 'tecnicas', 'ventajas']

	if elegido == 'habilidades':
		res = addNew(['Nivel', 'Stat','BonusTirado','BonusGuardado','Bonus', 'Descripcion'], True)
	
	with open(PATH_FOLDER + pjName, 'r') as file:
		char = eval(file.read())
		print('antes',char,S,S)
		char[elegido][res[0]]
		print('desp',char)
"""		
def askNew(pjName):
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	delet = ['name', 'raza', 'xp']
	newlyAdded = False
	# Generate a new list containing only those elements from clave that are not present in the delet
	clave_filtered = [key for key in claves if key not in delet]

	print('Que quieres agregar?: ')
	elegido = showAndChoose(clave_filtered, ['ATRAS'])

	if elegido == 'habilidades':
		newlyAdded = addNew(['Nivel', 'Stat', 'BonusTirado', 'BonusGuardado', 'Bonus', 'Descripcion'], True)
		
	pj[elegido].update(newlyAdded)  # Update existing habilidades with the new one
	
	if newlyAdded:
		with open(PATH_FOLDER + pjName, 'w') as file:	
			file.write(str(pj)) 
            
      
def addNew(lista, nombre = False):

	#lista is a array of things to cicle
	res = {}
	if nombre:
		nombre = input('Ingrese un nombre: ')
		res[nombre] = {}
	for i in lista:
		res[nombre][i] = input(f'Ingrese {i}: \n', )
	return res



def editPj(pjName):
	pj = getPj(pjName)
	claves = getPjKeys(pjName)
	print('Que quieres modificar?')
	primer = showAndChoose(claves, ['ATRAS'])
	if primer == 'ATRAS':
		opciones(primer, ORDEN[2], pjName)
		
	# If not dict, edit. If dict, ask again what
	if not isinstance(pj[primer], dict):
		pj[primer] = modificarString(pj[primer])
	else:
		primerList = list(pj[primer])
		for i in primerList:
			print(i, '  ', pj[primer][i], S )
		segundo = showAndChoose(primerList)
		
		#Is a Dict inside a Dict? Loop again
		if not isinstance(pj[primer][segundo], dict):
			pj[primer][segundo] = modificarString(pj[primer][segundo])
		else:
			segunList = list(pj[primer][segundo])
			for i in segunList:
				print(i, '  ', pj[primer][segundo][i], S )
			tercer = showAndChoose(segunList)
			
			if not isinstance(pj[primer][segundo][tercer], dict):
				pj[primer][segundo][tercer] = modificarString(pj[primer][segundo][tercer])
	
	with open(PATH_FOLDER + pjName, 'w') as file:
		file.write(str(pj))
	editPj(pjName)
	#Mejora: Debe haber una forma de cliclar esto, llamando a la misma funcion recursivamente

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
	#Cambiarlas de Array a Dict?
	habilidades = {}	
	hechizos = {}
	
	notas = {}
	notasEsp = {}
	tecnicas = {}
	ventajas = {}
	path = PATH_FOLDER+nombre
	#opciones = ['Habilidades','Tecnicas','Stats','Inventario']
	#Create file with character name
	with open(path, 'x') as file:
		personaje['name'] = nombre
		print('Vamos a crear paso a paso')
		#Raza
		personaje['raza'] = input('Ingrese la raza: ')
		
		#XP
		personaje['xp'] = {'usada':0,'disponible':0}
		print('Hay 2 tipos de XP, la usada y la disponible.')
		personaje['xp']['usada'] = input('Ingrese la xp usada: ')
		personaje['xp']['disponible'] = input('Ingrese la xp disponible: ')
		
		#Stats
		stats['Fuerza'] = input('Ingrese Fuerza: ')
		stats['Agilidad'] = input('Ingrese Agilidad: ')
		stats['Fe'] = input('Ingrese Fe: ')
		stats['Inteligencia'] = input('Ingrese Inteligencia: ')
		stats['Bravura'] = input('Ingrese Bravura: ')
		stats['Personalidad'] = input('Ingrese Personalidad: ')
	
		#print('Los hechizos y Habilidades los agregas en el panel de Personaje!')
		
		#Hechizos
		if input('Hechizo? y/any \n').lower() == 'y': hechizos = addHechizo()
		#hechizos = addHechizo()
		
		#Habilidades
		if input('Habilidad? y/any \n').lower() == 'y': habilidades = addHabilidad()
		#habilidades = addHabilidad()
		
		
		personaje['habilidades'] = habilidades
		personaje['hechizos'] = hechizos
		personaje['stats'] = stats
		personaje['notas'] = notas
		personaje['notasEsp'] = notasEsp
		personaje['tecnicas'] = tecnicas
		personaje['ventajas'] = ventajas
		file.write(str(personaje))
		print(personaje, '\n\n')
		
	checkForPjs()
			
		#Mostrar el nombre en grande del elegido junto con las opciones de Ver, Editar, Eliminar o Atras
		
#Remove Character FILE
def delPj():
	print('Cual deseas BORRAR?: ')
	eleccion = showPjs(['ATRAS'])
	if eleccion == 'ATRAS':
		opciones(eleccion, ORDEN[1])	
	else:
		path = PATH_FOLDER + eleccion
		if os.path.exists(path):
			os.remove(path)
			print('Archivo removido con exito')
		else:
			print("The file does not exist") 
	start()
		
def refreshFileName():
	pjs = os.listdir(PATH_FOLDER)
	for i in pjs:
		name = getPj(i)['name']
		if i != name:
			print(f'Nombre de archivo actualizado. De {i} a {name}')
			os.rename(PATH_FOLDER+i, PATH_FOLDER+name)
	atras(ORDEN[0])
	
def refresh():
	#os.system("gnome-terminal -e 'bash -c \"python3 pk.py; bash\" '")
	refreshFileName()
	os.system("gnome-terminal --command 'python3 pk.py';bash -c 'exit' ")
	
			
def start():
	#Greetings
	print('Bienvenido a PainKiller charactermancer by Facunchos')
	menu()

start()			
