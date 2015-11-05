""" Classes permettant la gestion et génération des niveaux du Jeu >BacMan: --- Adventures<"""

# Importation du module pygame et du fichier contenant les constantes du jeu

import pygame
from pygame.locals import *
from constantes.py import *

class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, level_file):

		self.level_file = level_file
		self.structure = 0

	def generation(self):
		""" Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher."""

		# Ouverture du fichier

		with open(self.level_file, 'r') as level_file:
			structure_level = []

			# Parcours des lignes du fichier
			for line in fichier:
				line_level = []

				# Parcours des sprites contenus dans le fichier
				for sprite in line:
					# On ignore les '\n' des fins de lignes
					if sprite != '\n':
						# Ajout de la ligne à la liste du level
						line_level.append(sprite)

				# On ajoute la liste de la ligne à la liste de la structure
				structure_level.append(line_level)

			# Sauvegarde de la structure
			self.structure = structure_level

########################
# Classes pour les cases
########################

class Square(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

class EmptySquare(Square):
	def __init__(self, has_power_pill):
		self.is_empty = True
		self.has_pill = True # Vaut True tant qu'une pillule est présente
		self.has_power_pill = has_power_pill # Vaut True si la pillule est une power pill

	def eat_pill(self):
		self.has_pill = False

		# mettre à jour le rendu graphique --> la pillule disparait

		#if self.has_power_pill:
		#lancer la fonction de la power pill --> ???


class Wall(Square):
	def __init__(self):
		self.is_empty = False

###########################
# Classes pour les pillules
###########################

class Pill(object):
	def __init__(self, square):
		self.points = 10

	def render(self):
		pass

class PowerPill(Pill):
	def __init__(self, square):
		Pill.__init__(self, square)
		### Compléter

	def render(self):
		pass

class BonusPill(Pill):
	def __init__(self, square):
		Pill.__init__(self, square)
		### Compléter

	def render(self):
		pass
