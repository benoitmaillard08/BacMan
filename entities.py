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
		"""
		Affiche le rendu de la case
		"""
		self.level.window.blit(self.picture, self.render_coords)

	def adjacent_square(self, index):
		"""
		Retourne la case adjacente dans la direction <index>
		L'index est un entier entre 0 et 3 --> 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		"""
		square_x = self.x + DIRECTIONS[index][0]
		square_y = self.y + DIRECTIONS[index][1]

		return self.level.get_square(square_x, square_y)

	def empty_adj_squares(self, direction):
		empty_adj_squares = [] # Listes des directions possibles (excepté la direction opposée)
					
		# On regarde si les cases à droite, devant et à gauche sont libres
		for n in range(-1, 2):
			test_dir = (direction + n) % 4
			adj = self.adjacent_square(test_dir)

			if adj and adj.is_empty: # si la case est libre, elle est ajoutée à la liste
				empty_adj_squares.append(test_dir)

		return empty_adj_squares


class StandardSquare(Square):
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = True # Le fantôme peut passer sur la case
		self.is_door = False # Les fantômes peuvent passer par la porte mais pas pacman
		self.pill = None
		self.picture = load_terrain("blank")
		self.tp = () # Coordonnées utilisés si la case permet la téléportation

	def add_pill(self, pill):
		"""
		Permet d'ajouter la pastille <pill> sur la case
		"""
		self.pill = pill

	def add_tp_coords(self, x, y):
		"""
		Transforme la case en point de téléportation vers les coordonnées <x> et <y>
		"""
		self.tp = (x, y)

	def eat(self):
		"""
		Supprime la pastille de la case et déclenche l'effet de celle-ci
		"""
		if self.pill:
			self.pill.effect()

			self.pill.sound.play() # Le son correspondant à la pastille est joué

			self.pill = None # La pillule est supprimée

			self.level.n_pills -= 1

			if self.level.n_pills == 0:
				self.level.master.end_level()

	def render(self):
		"""
		Affiche le rendu de la case
		"""
		self.level.window.blit(self.picture, self.render_coords)

		if self.pill:
			self.level.window.blit(self.pill.picture, self.render_coords)

class Wall(Square):
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case

	def select_picture(self):
		"""
		Définit l'image à utiliser d'après les cases adjacentes
		"""
		picture_code = ""

		# Vérifie le type des cases adjacentes dans les 4 directions
		for direction in range(4):
			adj = self.adjacent_square(direction)
			if not adj or adj.is_empty:
				picture_code += "0"
			else:
				picture_code += "1"

		self.picture = load_terrain(WALLS_PATTERN.format(picture_code))

class GhostDoor(StandardSquare):
		def __init__(self, level, x, y):
			StandardSquare.__init__(self, level, x, y)
			self.is_door = True

			self.picture = load_terrain("ghost-door")

##############################
# Classes pour les pastilles #
##############################

class Pill: pass

class StandardPill(Pill):
	def __init__(self, level):
		self.level = level
		self.points = 10 # Nombre de points gagnés avec le pellet
		self.picture = load_terrain("pellet") # Chargement de l'image
		self.sound = load_sound("pellet1")

	def effect(self):
		"""
		Augmente le score de la partie du nombre de points de la pastille
		"""
		self.level.master.update_score(self.points)
		self.sound.play()

class PowerPill(Pill):
	def __init__(self, level):
		self.level = level
		self.picture = load_terrain("pellet-power")
		self.sound = load_sound("powerpellet")

	def effect(self):
		"""
		Immobilise les fantômes pendant 100 tics
		"""
		for ghost in self.level.ghosts:
			ghost.stop(100)

class BonusPill(StandardPill):
	# Index de l'image et nombre de points correspondant aux niveaux jusqu'à 7
	TYPES = [(0, 100), (1, 300), (2, 500), (2, 500), (3, 700), (3, 700), (4, 1000)]

	def __init__(self, level):
		self.level = level
		self.sound = load_sound("eatfruit")


		# Si le niveau dépasse 7, ses caractéristiques sont les mêmes que le 7

		n_level = level.n_level

		if n_level > len(BonusPill.TYPES):
			n_level = 7

		# Sélection du tuple image - points par rapport au niveau
		bonus_type = BonusPill.TYPES[n_level-1]

		# Sélection de l'image et du bonus d'après le tuple
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

		# Vaut True lorsque le perso vient de se téléporter. Permet
		# d'éviter que le perso soit téléporté à nouveau immédiatement
		self.tp_flag = False

	def set_coords(self, x, y):
		"""
		Redéfinit les coordonnées du personnage
		"""
		self.x = x
		self.y = y

		# Les coordonnées initiales sont gardées en mémoire pour le respawn des personnages
		# Celles-ci prennent les valeurs en argument de cette fonction la première fois qu'elle est executée
		if self.init_x == -1 and self.init_y == -1:
			self.init_x = x
			self.init_y = y

	def reset(self):
		"""
		Permet de réinitialiser la position du personnage
		"""
		self.x = self.init_x
		self.y = self.init_y

	def render(self):
		"""
		Affiche le rendu du personnage
		"""
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
		"""
		Renvoie l'image correspondant au stade d'animation de pacman
		"""
		# Lorsque le stade 8 est atteint, l'index est remis à 0
		if self.n_frame > 8:
			self.n_frame = 0

		picture = self.pictures[self.direction][self.n_frame]

		if self.moving:
			self.n_frame += 1
		else: # Lorsque pacman est arrêté, celui-ci garde le stade 6
			self.n_frame = 6

		return picture

	def stop(self):
		"""
		Met en pause le mouvement de pacman
		"""
		self.moving = False

	def change_direction(self, direction):
		"""
		Permet de changer la direction de pacman
		"""
		self.next_direction = direction

	def move(self):
		"""
		Mouvement de Pacman
		"""
		# Si pacman se trouve exactement sur une case
		if self.x % 1 == 0 and self.y % 1 == 0:

			# Récupération de la case actuelle
			square = self.level.get_square(self.x, self.y)
			square.eat() # Pacman mange la pastille s'il y en a une
			
			# Si c'est une case de téléportation, Pacman se téléporte
			if square.tp and not self.tp_flag and self.moving:
				self.set_coords(*square.tp)
				self.tp_flag = True # On indique que pacman vient d'être tp

			else:
				# Case adjacente dans la direction souhaitée
				next_wanted = square.adjacent_square(self.next_direction)
				# Case adjacente dans la direction actuelle
				next = square.adjacent_square(self.direction)

				# Si la case dans la direction souhaitée est vide
				if next_wanted and next_wanted.is_empty and not next_wanted.is_door:
					self.direction = self.next_direction
					self.moving = True # Au cas où Pacman était arrêté, il repart

				# Si la case dans la direction actuelle est un mur, pacman s'arrête
				elif next and (not next.is_empty or next.is_door):
					self.stop()

				self.tp_flag = False # Pacman peut être téléporté à nouveau

		# Si Pacman n'est pas exactement sur une case, il
		# peut quand même rebrousser chemin
		elif abs(self.direction - self.next_direction) == 2:
			self.direction = self.next_direction

		# Modification des coordonnées selon la direction
		if self.moving and not self.tp_flag:
			# DIRECTIONS[self.directions] correspond au 
			# vecteur directeur de la trajectoire de Pacman
			self.x += self.speed * DIRECTIONS[self.direction][0] / SQUARE_SIZE
			self.y += self.speed * DIRECTIONS[self.direction][1] / SQUARE_SIZE

		self.check_ghosts()

	def check_ghosts(self):
		"""
		Gère les collisions avec les fantômes
		"""
		for ghost in self.level.ghosts:
			if abs(self.x - ghost.x) < 0.5 and abs(self.y - ghost.y) < 0.5:
				if ghost.pause > 0: # Si le fantômes est immobilisé
					ghost.pause = 0 # Le fantômes n'est plus immobilisé
					ghost.reset() # Le fantômes est renvoyé à sa position initiale
					load_sound('eatgh').play()



				else:
					self.level.pause_game(50) # Le jeu est mis en pause pour 50 tics

					self.level.master.update_lives() # Le nombre de vies de pacman est mis à jour

					# Pacman et les fantomes retournent à leur position initiale
					self.reset()
					for ghost in self.level.ghosts:
						ghost.reset()

				break




class Ghost(Char):
	def __init__(self, level):
		Char.__init__(self, level)

		self.direction = 0 # 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		self.speed = 8
		self.pause = 0

		self.pictures = []

		self.lane = []

	def load_picture(self):
		for n in range(1, 7):
			self.pictures.append(load_terrain(GHOST_PATTERN.format(self.name, n)))

		self.n_frame = 0

	def get_picture(self):
		"""
		Renvoie l'image correspondant au stade d'animation du fantômes
		"""
		if self.n_frame > 5:
			self.n_frame = 0

		picture = self.pictures[self.n_frame]

		self.n_frame += 1

		return picture

	def move(self):
		"""
		Mouvement du fantôme
		"""
		if self.pause == 0:
			# Si le fantôme se trouve exactement sur une case
			if self.x % 1 == 0 and self.y % 1 == 0:
				# Récupération de la case actuelle
				square = self.level.get_square(self.x, self.y)

				# Si c'est une case de téléportation, le fantôme se téléporte
				if square.tp and not self.tp_flag:
					self.set_coords(*square.tp)
					self.tp_flag = True # Indique que le fantome vient d'être téléporté

				else:
					# new_dir = self.reach_square(square, self.level.get_square(1, 1), self.direction)
					# print(self.level.get_square(1, 1))

					# if new_dir:
					# 	print("new dir : " + str(new_dir))
					# 	self.direction = new_dir

					# else:
						
					empty_adj_squares = square.empty_adj_squares(self.direction)

					# Si les cases devant et sur les côtés sont occupées, le fantôme rebrousse chemin
					if len(empty_adj_squares) == 0:
						self.direction = (self.direction + 2) % 4

					# Sinon, une directions est choisie aléatoirement dans celles qui sont possibles
					else:
						self.direction = empty_adj_squares[random.randint(0, len(empty_adj_squares) - 1)]

					self.tp_flag = False # Le fantôme peut à nouveau être téléporté

			if not self.tp_flag: # Le fantôme doit attendre un tic pour bouger après une téléportation
				self.x += self.speed * DIRECTIONS[self.direction][0] / SQUARE_SIZE
				self.y += self.speed * DIRECTIONS[self.direction][1] / SQUARE_SIZE
		else:
			self.pause -= 1

	def reach_square(self, square, objective, direction):

		# Si la case actuelle correspond à la case visée, l'objectif est atteint
		if square == objective:
			return direction

		else:
			empty_adj_squares = square.empty_adj_squares(direction)

			# S'il s'agit d'un cul de sac, il faut revenir en arrière
			if len(empty_adj_squares) == 0:
				return None

			else:
				for new_dir in empty_adj_squares:
					next_square = square.adjacent_square(new_dir)

					if self.reach_square(next_square, objective, new_dir):
						return new_dir

					
				return None



	def stop(self, time):
		"""
		Met le fantôme en pause pour une certaine durée
		"""
		self.pause = time

class Blinky(Ghost):
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "blinky"

		self.load_picture()

class Pinky(Ghost):
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "pinky"
		

		self.load_picture()

class Clyde(Ghost):
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "clyde"

		self.load_picture()

class Inky(Ghost):
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "inky"

		self.load_picture()