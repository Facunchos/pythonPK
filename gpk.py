import os
import subprocess
from tabulate import tabulate

# Constants
STATS = ('Fuerza', 'Agilidad', 'Fe', 'Entendimiento', 'Bravura', 'Personalidad')
ORDEN = ['MENU', 'SHOWPJS', 'PJ', 'EDITPJ']
INFO_CON_NOMBRE = {'habilidades': ['Nivel', 'Stat', 'BonusTirado', 'BonusGuardado', 'Bonus', 'Descripcion'],
                   'hechizos': ['Descripcion'], 'tecnicas': ['Detalle'], 'ventajas': ['Detalle']}
INFO_SIN_NOMBRE = {'notas': ['Detalle'], 'notasEsp': ['Detalle']}
PATH_FOLDER = './pjs/'
S = '\n'

def checkFolder():
    """Check for the folder. If it doesn't exist, create it."""
    if not os.path.isdir(PATH_FOLDER):
        os.makedirs(PATH_FOLDER)
        print('Se ha creado la carpeta "pjs" para almacenar los personajes')

def listPJ():
    """List all files in the pjs folder."""
    checkFolder()
    return os.listdir(PATH_FOLDER)

def showAndChoose(options):
    """Display options and return user choice."""
    print(S)
    for i, option in enumerate(options):
        print(f"{i} - {option}")
    while True:
        choice = input('Elija uno: ')
        if choice.isdigit() and 0 <= int(choice) < len(options):
            return options[int(choice)]
        print('Ingrese un número válido.')

def start():
    """Start the program."""
    print('Bienvenido a PainKiller charactermancer by Facunchos')
    any()
    menu()

def any():
    """Wait for user input."""
    print(S)
    input('Presione cualquier tecla para continuar')

def menu():
    """Display the main menu."""
    inicio = ['Personajes', 'Manual', 'Hoja Excel', 'Creditos', 'Cafesito', 'Refresh File names']
    links = {'Manual': 'https://drive.google.com/drive/u/0/folders/1cLwQJNBNFOMCxDp7t_fC4DHqz9kdyJUA',
             'Hoja Excel': 'https://docs.google.com/spreadsheets/d/1CA0mS23IgUdEZ-WnBhtf66BKSf_Mvkb83Yp-YzjG7uQ/edit#gid=2043668604',
             'Creditos': 'Creado por Facundo Martinez (Facunchos) En 2024 \nLinkedin: \nhttps://www.linkedin.com/in/facunmartinez/ \nGitHub: \nhttps://github.com/Facunchos',
             'Cafesito': 'Hacerme cuenta de Cafesito!'}
    choice = showAndChoose(inicio)
    if choice in links:
        print(links[choice])
        menu()
    elif choice == 'Personajes':
        checkForPjs()
    elif choice == 'Refresh File names':
        refreshFileName()
    else:
        print('Elija una opcion correcta')
        menu()

def checkForPjs():
    """Check for existing characters."""
    eleccion = showPjs(['ATRAS'])
    if eleccion == 'ATRAS':
        menu()
    else:
        print('Haz elegido:', eleccion)
        showPjInfo(eleccion)

def showPjInfo(pjName):
    """Display information about a character."""
    # Implement as needed
    pass

def showPjs(opt=None):
    """List characters and return user choice."""
    return showAndChoose(listPJ(), opt)

def refreshFileName(backToMenu=True):
    """Refresh file names in the pjs folder."""
    pjs = os.listdir(PATH_FOLDER)
    for pj in pjs:
        name = getPj(pj)['name']
        if pj != name:
            print(f'Nombre de archivo actualizado. De {pj} a {name}')
            os.rename(os.path.join(PATH_FOLDER, pj), os.path.join(PATH_FOLDER, name))
    if backToMenu:
        menu()

def getPj(pjName):
    """Get character data."""
    with open(os.path.join(PATH_FOLDER, pjName)) as file:
        return eval(file.read())

def opciones(el, orden=None, pjName=None, esPJ=False):
    """Process user options."""
    pass  # Implement as needed

def addPj():
    """Add a new character."""
    pass  # Implement as needed

def delPj():
    """Delete a character."""
    pass  # Implement as needed

if __name__ == "__main__":
    start()
