""" Classes permettant la gestion et génération des niveaux du Jeu >BacMan: --- Adventures<"""

# Importation du module pygame et du fichier contenant les constantes du jeu

import pygame
from pygame.locals import *
import constantes

class Level:
	"""Classe permettant de créer un niveau"""
	
	# Définit les classes à utiliser pour les différents types de cases sans mur
	ELEMENTS = {
		STANDARD_PILL = Empt
	}


	def __init__(self, level_filename):

		self.level_filename = filename
		self.structure = 

	def generation(self):
		""" Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher."""

		# Ouverture du fichier

		level_file = open(self.level_filename, 'r')
		content = level.read()

		l_lines = content.split("\n")

		for line in l_lines:
			line_level = []
			square = None

			for char in line:
				if char in Level.EMPTY_SQUARES:
					square = EmptySquare(pill = Level.EMPTY_SQUARES)


			# structure_level = []

			# # Parcours des lignes du fichier
			# for line in fichier:
			# 	line_level = []

			# 	# Parcours des sprites contenus dans le fichier
			# 	for sprite in line:
			# 		# On ignore les '\n' des fins de lignes
			# 		if sprite != '\n':
			# 			# Ajout de la ligne à la liste du level
			# 			line_level.append(sprite)

			# 	# On ajoute la liste de la ligne à la liste de la structure
			# 	structure_level.append(line_level)

			# # Sauvegarde de la structure
			# self.structure = structure_level

########################
# Classes pour les cases
########################

class Square(object):
	def __init__(self):
		pass

	def render(self):
		pass

		## Rendu de la case

class EmptySquare(Square):
	def __init__(self, pill):
		Square.__init__(self)
		self.is_empty = True # Le fantôme peut passer sur la case

class Wall(Square):
	def __init__(self):
		Square.__init__(self)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case

###########################
# Classes pour les pillules
###########################

class Pill(EmptySquare): # Classe abstraite
	def __init__(self):
		EmptySquare.__init__(self)
		self.pill_eaten = False

	def eat(self):
		self.pill_eaten = True
		self.picture = "" # Redevient une case vide

		self.effect()

	def effect(self):
		pass

class StandardPill(Pill):
	def __init__(self):
		Pill.__init__(self)
		self.points = 10
		self.picture = ""

	def effect(self):
		pass
		## Augmentation des points

class PowerPill(Pill):
	def __init__(self):
		Pill.__init__(self)
		self.picture = ""

	def effect():
		pass
		## Les fantômes s'arrêtent

class BonusPill(StandardPill):
	def __init__(self):
		Pill.__init__(self)
		
		##### Valeur et image
