import pygame
from constantes import *
from shortcuts import *

##########################
# Classes pour les cases #
##########################

class Square:
	INDEXES = [(0, -1), (1, 0), (0, 1), (-1, 0)]
	def __init__(self, level, x, y):
		self.level = level
		self.x = x
		self.y = y

		# Coordonés en pixel du coin supérieur gauche
		self.render_coords = (self.x*16, self.y*16)

	def render(self):
		pass

	def adjacent_square(self, index): # L'index est un entier entre 0 et 3 --> 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		square_x = self.x + Square.INDEXES[index][0]
		square_y = self.y + Square.INDEXES[index][1]

		return self.level.get_square(square_x, square_y)

class StandardSquare(Square):
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = True # Le fantôme peut passer sur la case
		self.pill = None
		self.picture = load_terrain("blank")

	def add_pill(self, pill):
		self.pill = pill

	def eat(self):
		self.pill.effect()
		self.pill = None # La pillule est supprimée

	def render(self):
		self.level.window.blit(self.picture, self.render_coords)

		if self.pill:
			self.level.window.blit(self.pill.picture, self.render_coords)

class Wall(Square):
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case

	def select_picture(self):
		picture_code = ""

		for n in range(4):
			adj = self.adjacent_square(n)
			if not adj or adj.is_empty:
				picture_code += "0"
			else:
				picture_code += "1"

		self.picture = load_terrain(WALLS_PATTERN.format(picture_code))

	def render(self):
		self.level.window.blit(self.picture, self.render_coords)


##############################
# Classes pour les pastilles #
##############################

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

################################
# Classes pour les personnages #
################################

class Char
	def __init__(self):
		pass

	def set_coords(self, x, y):
		self.x = x
		self.y = y

class PacMan(Char):
	PICTURE_DIRECTIONS = ("u", "r", "d", "l")

	def __init__(self):
		self.direction = 0 # 0 = haut, 1 = droite, 2 = bas, 3 = gauche


		# Liste à deux dimensions qui contiendra les images des différents "stades"
		# d'ouverture de la bouche de pacman
		self.pictures = []

		for d in PacMan.PICTURE_DIRECTIONS:
			# L'image de pacman avec la bouche fermée est placée en index 0 de chaque direction
			picture_closed = load_terrain(PACMAN_PATTERN.format("",""))
			direction_pictures = [picture_closed]

			# Pour chaque direction, on charge les images de 1 à 8
			for n in range(1, 9):
				direction_pictures.append(load_terrain(PACMAN_PATTERN.format(d, n)))

			self.pictures.append(direction_pictures)

		self.n_frame = 0 # Index de l'image à utiliser 

	def get_picture(self):
		if self.n_frame > 8:
			self.n_frame = 0

		picture = self.pictures[self.direction][self.n_frame]

		self.n_frame += 1

		return picture

	def render(self):




class Monster(Char): pass