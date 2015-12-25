import pygame
import random
from constantes import *
from shortcuts import *

##########################
# Classes pour les cases #
##########################

class Square:
	def __init__(self, level, x, y):
		self.level = level
		self.x = x
		self.y = y

		# Coordonés en pixel du coin supérieur gauche
		self.render_coords = (self.x*SQUARE_SIZE, self.y*SQUARE_SIZE)

	def render(self):
		pass

	def adjacent_square(self, index): # L'index est un entier entre 0 et 3 --> 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		square_x = self.x + DIRECTIONS[index][0]
		square_y = self.y + DIRECTIONS[index][1]

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
		if self.pill:
			self.pill.effect()
			self.pill = None # La pillule est supprimée

			self.level.n_pills -= 1

			if self.level.n_pills == 0:
				self.level.game.end_level()

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
		self.level = level
		self.points = 10 # Nombre de points gagnés avec le pellet
		self.picture = load_terrain("pellet") # Chargement de l'image

	def effect(self):
		self.level.game.update_score(self.points)

class PowerPill(Pill):
	def __init__(self, level):
		self.level = level
		self.picture = load_terrain("pellet-power")

	def effect(self):
		for ghost in self.level.ghosts:
			ghost.stop(100)

class BonusPill(StandardPill):
	# Index de l'image et nombre de points correspondant aux niveaux jusqu'à 7
	TYPES = [(0, 100), (1, 300), (2, 500), (2, 500), (3, 700), (3, 700), (4, 1000)]

	def __init__(self, level):
		self.level = level
		# Si le niveau dépasse 7, ses caractéristiques sont les mêmes que le 7

		n_level = level.n_level

		if n_level > len(BonusPill.TYPES):
			n_level = 7

		# Sélection du tuple image - points par rapport au niveau
		bonus_type = BonusPill.TYPES[n_level-1]

		self.picture = load_terrain(FRUIT_PATTERN.format(bonus_type[0]))
		self.points = bonus_type[1]

################################
# Classes pour les personnages #
################################

class Char:
	def __init__(self, level):
		self.level = level

		self.init_x = -1
		self.init_y = -1

	def set_coords(self, x, y):
		self.x = x
		self.y = y

		if self.init_x == -1 and self.init_y == -1:
			self.init_x = x
			self.init_y = y

	def reset(self):
		self.x = self.init_x
		self.y = self.init_y

	def render(self):
		self.level.window.blit(self.get_picture(), (self.x*SQUARE_SIZE, self.y*SQUARE_SIZE))

class PacMan(Char):
	PICTURE_DIRECTIONS = ("u", "r", "d", "l")

	def __init__(self, level):
		Char.__init__(self, level)

		self.speed = 8

		self.direction = 1 # 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		self.next_direction = 1 # Direction que prendra pacman dès qu'un carrefour le permet
		self.moving = True # Vaut True si Pacman est en mouvement


		# Liste à deux dimensions qui contiendra les images des différents "stades"
		# d'ouverture de la bouche de pacman
		self.pictures = []

		for d in PacMan.PICTURE_DIRECTIONS:
			# L'image de pacman avec la bouche fermée est placée en index 0 de chaque direction
			picture_closed = load_terrain("pacman")
			direction_pictures = [picture_closed]

			# Pour chaque direction, on charge les images de 1 à 8
			for n in range(1, 9):
				direction_pictures.append(load_terrain(PACMAN_PATTERN.format(d, n)))

			self.pictures.append(direction_pictures)

		self.n_frame = 6 # Index de l'image à utiliser 

	def get_picture(self):
		# Lorsque le stade 8 est atteint, l'index est remis à 0
		if self.n_frame > 8:
			self.n_frame = 0

		picture = self.pictures[self.direction][self.n_frame]

		if self.moving:
			self.n_frame += 1
		else:
			self.n_frame = 6

		return picture

	def stop(self):
		self.moving = False

	def change_direction(self, direction):
		self.next_direction = direction

	def move(self):
		# Si pacman se trouve exactement sur une case
		if self.x % 1 == 0 and self.y % 1 == 0:
			# Récupération de la case actuelle
			square = self.level.get_square(self.x, self.y)
			square.eat() # Pacman mange la pastille s'il y en a une

			# Si la case dans la direction souhaitée est vide
			if square.adjacent_square(self.next_direction).is_empty:
				self.direction = self.next_direction
				self.moving = True # Au cas où Pacman était arrêté, il repart

			# Si la case dans la direction actuelle est un mur, pacman s'arrête
			elif not square.adjacent_square(self.direction).is_empty:
				self.stop()

		# Si Pacman n'est pas exactement sur une case, il
		# peut quand même rebrousser chemin
		elif abs(self.direction - self.next_direction) == 2:
			self.direction = self.next_direction

		# Modification des coordonnées selon la direction
		if self.moving:
			# DIRECTIONS[self.directions] correspond au 
			# vecteur directeur de la trajectoire de Pacman
			self.x += self.speed * DIRECTIONS[self.direction][0] / SQUARE_SIZE
			self.y += self.speed * DIRECTIONS[self.direction][1] / SQUARE_SIZE

		self.check_ghosts()

	def check_ghosts(self):
		for ghost in self.level.ghosts:
			if abs(self.x - ghost.x) < 0.5 and abs(self.y - ghost.y) < 0.5:
				if ghost.pause > 0:
					ghost.pause = 0
					ghost.reset()
				else:
					self.level.pause_game(50)
					self.reset()
					for ghost in self.level.ghosts:
						ghost.reset()

					self.level.game.update_lives()

				break




class Ghost(Char):
	def __init__(self, level):
		Char.__init__(self, level)

		self.direction = 0
		self.speed = 8
		self.pause = 0

		self.pictures = []

		for n in range(1, 7):
			self.pictures.append(load_terrain(GHOST_PATTERN.format(n)))

		self.n_frame = 0

	def get_picture(self):
		if self.n_frame > 5:
			self.n_frame = 0

		picture = self.pictures[self.n_frame]

		self.n_frame += 1

		return picture

	def move(self):
		if self.pause == 0:
			# Si le fantôme se trouve exactement sur une case
			if self.x % 1 == 0 and self.y % 1 == 0:
				# Récupération de la case actuelle
				square = self.level.get_square(self.x, self.y)

				empty_adj_squares = []

				for n in range(-1, 2):
					direction = (self.direction + n) % 4
					if square.adjacent_square(direction).is_empty:
						empty_adj_squares.append(direction)

				if len(empty_adj_squares) == 0:
					self.direction = (self.direction + 2) % 4

				else:
					self.direction = empty_adj_squares[random.randint(0, len(empty_adj_squares) - 1)]

			self.x += self.speed * DIRECTIONS[self.direction][0] / SQUARE_SIZE
			self.y += self.speed * DIRECTIONS[self.direction][1] / SQUARE_SIZE
		else:
			self.pause -= 1

	def stop(self, time):
		self.pause = time

class Blinky(Ghost): pass

class Pinky(Ghost): pass

class Clyde(Ghost): pass

class Inky(Ghost): pass