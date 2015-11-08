""" Classes permettant la gestion et génération des niveaux du Jeu >BacMan the baccalaureates Adventure!< """

# Importation du module pygame et du fichier contenant les constantes du jeu

import pygame
from pygame.locals import *
import constantes

class Level:
	SQUARES = {
		"#" : Wall,
		"*" : StandardPill,
		"%" : PowerPill,
		"+" : BonusPill,
	}

	CHARS = {
		"M" : PacMan,
		"B" : Blinky,
		"P" : Pinky,
		"I" : Inky,
		"C" : Clyde,
	}

	"""Classe permettant de créer un niveau"""
	
	# Définit les classes à utiliser pour les différents types de cases sans mur
	


	def __init__(self, level_filename):

		self.level_filename = filename
		self.structure = []

	def generation(self):
		""" Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher."""

		### Penser à gérer les erreurs en cas d'anomalité dans le fichier de level

		# Ouverture du fichier
		level_file = open(self.level_filename, 'r')
		content = level_file.read()

		l_lines = content.split("\n")

		for line in l_lines:
			level_line = []
			square = None

			for char in line:
				if char in Level.SQUARES:
					square = Level.SQUARES[char]

				elif char in Level.CHARS:
					# Instanciation du perso

					square = EmptySquare()

				else:
					pass ### Penser à lever une exception ici

				line_level.append(square) # La case es ajoutée à la ligne

			self.structure.append()


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
	def __init__(self):
		Square.__init__(self)
		self.is_empty = True # Le fantôme peut passer sur la case

class Wall(Square):
	def __init__(self):
		Square.__init__(self)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case
		self.pill = False # Il n'y a pas de pillule

###########################
# Classes pour les pillules
###########################

class Pill(EmptySquare): # Classe abstraite
	def __init__(self):
		EmptySquare.__init__(self)
		self.pill = True

	def eat(self):
		self.pill = False # La pillule n'est plus là
		self.picture = "" # Redevient une case vide

		self.effect()

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

##############################
# Classes pour les personnages
##############################

class PacMan()
