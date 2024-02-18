import os
import numpy as np

statsTuple = ('Fuerza','Agilidad','Fe','Entendimiento','Bravura','Personalidad')
ANE = ['ATRAS','NUEVO','EDITAR']
ABN = ['ATRAS','BORRAR','NUEVO']
ABNE = ['ATRAS','BORRAR','NUEVO','EDITAR']
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
		

listPjs = checkFolder()
#If no pjs, create the first
def checkForPjs():
	#Check if the pjs folder is created. If not create one
	checkFolder()
	#Show all the characters avairable
	eleccion = showPjs(ABN)
	print('Haz elejido a : ',eleccion)
	
	if eleccion == 'ATRAS':
		menu()
	elif eleccion == 'BORRAR':
		seguro = input('ESTAS SEGURO? y/any \n')
		if seguro.lower() == 'y':
			delPj()
	elif eleccion == 'NUEVO':
		addPj()
	else:
		"""
		file = open(PATH_FOLDER+personajeElegido)
		print(file.read())
		file.close()
		"""
		#showAndChoose( ['STATS','HABILIDADES','HECHIZOS','NOTAS','NOTAS ESP','TECNICAS','VENTAJAS'], ANE)
		showPj(eleccion)
		#Agregar opciones
		
	# Hacer una funcion aparte para esto
def showPj(pj):
	opciones = []
	with open(PATH_FOLDER + pj, 'r') as file:
		personaje = file.readlines()
		#	print(personaje['name'], S)
		for i in personaje:
			print(personaje[i], S)
			#print(personaje[i])


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
	inicio = ['Personajes', 'Manual','Hoja Excel','Creditos','Cafesito', 'Refresh']
	elegido = showAndChoose(inicio)
	
	
	if elegido == 'Manual':
		print(link('https://drive.google.com/drive/u/0/folders/1cLwQJNBNFOMCxDp7t_fC4DHqz9kdyJUA'))
		menu()
	elif elegido == 'Hoja Excel':
		print(link('https://docs.google.com/spreadsheets/d/1CA0mS23IgUdEZ-WnBhtf66BKSf_Mvkb83Yp-YzjG7uQ/edit#gid=2043668604'))
		menu()
	elif elegido == 'Creditos':
		print('Creado por Facundo Martinez (Facunchos) En 2024')
		print('Linkedin: ')
		print(link('https://www.linkedin.com/in/facunmartinez/'))
		print('GitHub: ')
		print(link('https://github.com/Facunchos'))
		menu()
	elif elegido == 'Cafesito':
		print('Hacerme cuenta de Cafesito!')
		menu()
	elif elegido == 'Personajes':
		checkForPjs()
	elif elegido == 'Refresh':
		refresh()
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
		start()	
	else:
		path = PATH_FOLDER + eleccion
		if os.path.exists(path):
			os.remove(path)
			print('Archivo removido con exito')
		else:
			print("The file does not exist") 
	start()
		
#def editPj():
def refresh():
	#os.system("gnome-terminal -e 'bash -c \"python3 pk.py; bash\" '")
	os.system("gnome-terminal --command 'python3 pk.py';bash -c 'exit' ")

def start():
	#Greetings
	print('Bienvenido a PainKiller charactermancer by Facunchos')
	menu()

start()			
