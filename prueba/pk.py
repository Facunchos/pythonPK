import os
import numpy as np
import time
import sys
import subprocess
from tabulate import tabulate

def leer():
	with open('Joshua') as file:
		return file.read()

def inicio():
	print(leer())
inicio()
