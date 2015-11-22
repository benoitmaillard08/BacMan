import pygame
import constantes
from shortcuts import *

########################
# Classes pour les cases
########################

class Square:
	def __init__(self, level, x, y):
		self.level = level
		self.x = x
		self.y = y

class StandardSquare(Square):
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = True # Le fantôme peut passer sur la case
		self.pill = None

	def add_pill(self, pill):
		self.pill = pill

	def eat(self):
		self.pill.effect()
		self.pill = None # La pillule est supprimée

	def render(self):
		###

		if self.pill:
			pass
			###

class Wall(Square):
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case

###########################
# Classes pour les pillules
###########################

class Pill: pass

class StandardPill(Pill):
	def __init__(self, level):
		self.points = 10 # Nombre de points gagnés avec le pellet
		self.picture = load_terrain("pellet") # Chargement de l'image

	def effect(self):
		pass
		## Augmentation des points

class PowerPill(Pill):
	def __init__(self, level):
		self.picture = load_terrain("pellet-power")

	def effect(self):
		pass
		## Les fantômes s'arrêtent

class BonusPill(StandardPill):
	# Index de l'image et nombre de points correspondant aux niveaux jusqu'à 7
	TYPES = [(0, 100), (1, 300), (2, 500), (2, 500), (3, 700), (3, 700), (4, 1000)]

	def __init__(self, level):
		# Si le niveau dépasse 7, ses caractéristiques sont les mêmes que le 7

		n_level = level.n_level

		if n_level > len(BonusPill.TYPES):
			n_level = 7

		# Sélection du tuple image - points par rapport au niveau
		bonus_type = BonusPill.TYPES[n_level-1]

		self.picture = load_terrain("fruit {}".format(bonus_type[0]))
		self.points = bonus_type[1]