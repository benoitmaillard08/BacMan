import pygame
import random
from constantes import *
from shortcuts import *

##########################
# Classes pour les cases #
##########################

class Square:
	"""
	Classe abstraite représentant une case du jeu
	"""
	def __init__(self, level, x, y):
		self.level = level
		self.x = x
		self.y = y

		# Coordonés en pixel du coin supérieur gauche
		self.render_coords = (self.x*SQUARE_SIZE, self.y*SQUARE_SIZE)

	def render(self):
		"""
		render() --> None
		Affiche le rendu de la case
		"""
		self.level.window.blit(self.picture, self.render_coords)

	def adjacent_square(self, index):
		"""
		adjacent_square(int index) --> Square
		Retourne la case adjacente dans la direction <index>
		L'index est un entier entre 0 et 3 --> 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		"""
		square_x = self.x + DIRECTIONS[index][0]
		square_y = self.y + DIRECTIONS[index][1]

		return self.level.get_square(square_x, square_y)

	def empty_adj_squares(self, direction):
		"""
		empty_adj_squares(int direction) --> int
		Retourne les directions possibles (0,1,2,3) vers les cases adjacentes excepté
		la direction opposée à la direction actuelle 
		"""
		empty_adj_squares = []
					
		# On regarde si les cases à droite, devant et à gauche sont libres
		for n in range(-1, 2):
			test_dir = (direction + n) % 4
			adj = self.adjacent_square(test_dir)

			if adj and adj.is_empty: # si la case est libre, elle est ajoutée à la liste
				empty_adj_squares.append(test_dir)


		return empty_adj_squares

	def __add__(self, tuple_add):
		"""
		__add__(tuple tuple_add) --> Square
		Retourne la case augmentée/diminuée des valeurs de tuple_add

		"""
		x = self.x + tuple_add[0]
		y = self.y + tuple_add[1]

		return self.level.get_square(x, y)


class StandardSquare(Square):
	"""
	Classe représentant une case sans mur
	"""
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = True # Le fantôme peut passer sur la case
		self.is_door = False # Les fantômes peuvent passer par la porte mais pas pacman
		self.pill = None
		self.picture = load_terrain("blank")
		self.tp = () # Coordonnées utilisés si la case permet la téléportation

	def add_pill(self, pill):
		"""
		add_pill(Pill pill) --> None
		Permet d'ajouter la pastille <pill> sur la case
		"""
		self.pill = pill

	def add_tp_coords(self, x, y):
		"""
		add_tp_coords(int x, int y) --> None
		Transforme la case en point de téléportation vers les coordonnées <x> et <y>
		"""
		self.tp = (x, y)

	def eat(self):
		"""
		eat() --> None
		Supprime la pastille de la case et déclenche l'effet de celle-ci
		"""
		if self.pill: # Effet de la pillule
			self.pill.effect()

			self.pill.sound.play() # Le son correspondant à la pastille est joué

			self.pill = None # La pillule est supprimée

			self.level.n_pills -= 1

			# S'il n'y a plus la moindre pastille, le niveau est terminé
			if self.level.n_pills == 0:
				self.level.master.end_level()

	def render(self):
		"""
		render() --> None
		Affiche le rendu de la case
		"""
		self.level.window.blit(self.picture, self.render_coords)

		if self.pill:
			self.level.window.blit(self.pill.picture, self.render_coords)

class Wall(Square):
	"""
	Classe représentant une case contenant un mur
	"""
	def __init__(self, level, x, y):
		Square.__init__(self, level, x, y)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case

	def select_picture(self):
		"""
		select_picture() --> None
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
	"""
	Classe représentant une case contenant une porte
	Seuls les fantômes peuvent traverser cette case
	"""
	def __init__(self, level, x, y):
		StandardSquare.__init__(self, level, x, y)
		self.is_door = True

		self.picture = load_terrain("ghost-door")

##############################
# Classes pour les pastilles #
##############################

class Pill: pass

class StandardPill(Pill):
	"""
	Classe représentant une pastille standard
	"""
	def __init__(self, level):
		self.level = level
		self.points = 10 # Nombre de points gagnés avec le pellet
		self.picture = load_terrain("pellet") # Chargement de l'image
		self.sound = load_sound("pellet1")

	def effect(self):
		"""
		effet() --> None
		Augmente le score de la partie du nombre de points de la pastille
		"""
		self.level.master.update_score(self.points)
		self.sound.play()

class PowerPill(Pill):
	"""
	Classe représentant une pastille de puissance qui endort
	momentanément les fantômes
	"""
	def __init__(self, level):
		self.level = level
		self.picture = load_terrain("pellet-power")
		self.sound = load_sound("powerpellet")

	def effect(self):
		"""
		effect() --> None
		Immobilise les fantômes pendant 100 tics
		"""
		for ghost in self.level.ghosts:
			ghost.stop(100)

class BonusPill(StandardPill):
	"""
	Classe représentant une pastille fruit qui rapporte un plus
	grand nombre de points à pacman
	"""
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
	"""
	Classe abstraite représentant un personnage du jeu
	"""
	def __init__(self, level):
		self.level = level

		self.init_x = -1
		self.init_y = -1

		# Vaut True lorsque le perso vient de se téléporter. Permet
		# d'éviter que le perso soit téléporté à nouveau immédiatement
		self.tp_flag = False

	def set_coords(self, x, y):
		"""
		set_coords(int x, int y) --> None
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
		reset() --> None
		Permet de réinitialiser la position du personnage
		"""
		self.x = self.init_x
		self.y = self.init_y

	def render(self):
		"""
		render() --> None
		Affiche le rendu du personnage
		"""
		self.level.window.blit(self.get_picture(), (self.x*SQUARE_SIZE, self.y*SQUARE_SIZE))

class PacMan(Char):
	"""
	Classe représentant Pacman
	"""
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
		get_picture() --> pygame.image
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
		stop() --> None
		Met en pause le mouvement de pacman
		"""
		self.moving = False

	def change_direction(self, direction):
		"""
		change_direction(int direction)
		Permet de changer la direction de pacman
		"""
		self.next_direction = direction

	def move(self):
		"""
		move() --> None
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
		check_ghosts() --> None
		Gère les collisions avec les fantômes
		"""
		for ghost in self.level.ghosts:
			if abs(self.x - ghost.x) < 0.5 and abs(self.y - ghost.y) < 0.5:
				if ghost.pause > 0: # Si le fantômes est immobilisé
					ghost.pause = 0 # Le fantômes n'est plus immobilisé
					ghost.reset() # Le fantômes est renvoyé à sa position initiale

					self.level.master.update_score(ghost.points)

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
	"""
	Classe abstraite représentant un fantôme
	"""
	def __init__(self, level):
		Char.__init__(self, level)

		self.direction = 0 # 0 = haut, 1 = droite, 2 = bas, 3 = gauche
		self.speed = 8
		self.pause = 0

		self.pictures = []

		self.lane = []

	def load_picture(self):
		"""
		load_picture() --> None

		Charge l'image associée au fantôme
		"""
		for n in range(1, 7):
			self.pictures.append(load_terrain(GHOST_PATTERN.format(self.name, n)))

		self.n_frame = 0

	def get_picture(self):
		"""
		get_picture() --> pygame.image
		Renvoie l'image correspondant au stade d'animation du fantômes
		"""
		if self.n_frame > 5:
			self.n_frame = 0

		picture = self.pictures[self.n_frame]

		self.n_frame += 1

		return picture

	def move(self):
		"""
		move() --> None
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
					self.set_direction(square)

					self.tp_flag = False # Le fantôme peut à nouveau être téléporté

			if not self.tp_flag: # Le fantôme doit attendre un tic pour bouger après une téléportation
				self.x += self.speed * DIRECTIONS[self.direction][0] / SQUARE_SIZE
				self.y += self.speed * DIRECTIONS[self.direction][1] / SQUARE_SIZE
		else:
			self.pause -= 1

	def random_direction(self, square, fav_direction=-1):
		"""
		random_direction(Square square, int fav_direction)
		Donne au fantôme une direction aléatoire lorsque la direction
		prioritaire fav_direction n'est pas disponible (si elle existe)
		"""
		empty_adj_squares = square.empty_adj_squares(self.direction)

		# Si les cases devant et sur les côtés sont occupées, le fantôme rebrousse chemin
		if len(empty_adj_squares) == 0:
			self.direction = (self.direction + 2) % 4

		# S'il y a une direction prioritaire possible, on la prend
		elif fav_direction >= 0 and fav_direction in empty_adj_squares:
			self.direction = fav_direction

		# Sinon, une direction est choisie aléatoirement dans celles qui sont possibles
		else:
			self.direction = empty_adj_squares[random.randint(0, len(empty_adj_squares) - 1)]

	def distance_from(self, square, objective):
		"""
		distance_from(Square square, Square objective) --> int
		Renvoie la distance entre les cases square et objective
		"""
		# distance par rapport à l'objectif
		diff_x = objective.x - self.x
		diff_y = objective.y - self.y

		return ((diff_x)**2 + (diff_y)**2)**0.5

	def get_to_square(self, square, objective):
		"""
		get_to_square(Square square, Square objective) --> None
		Permet au fantôme d'essayer d'atteindre l'objectif 
		objective
		"""

		# Si la distance vaut moins que 10, on tente le backtracking
		if self.distance_from(square, objective) < 15:
			new_dir = self.backtracking(square, objective, self.direction)

			if new_dir >= 0 and not (square.x, square.y) == (objective.x, objective.y):
				self.direction = new_dir
			else:
				self.random_direction(square)

		# Sinon, on cherche la meilleure direction à prendre pour
		# s'approcher de l'objectif
		else:
			# Si la différence en abscisse est plus
			# importante, on tente de réduire celle-ci
			if abs(objective.x - self.x) > abs(objective.y - self.y):
				if objective.x - self.x > 0:
					fav_direction = 1

				else:
					fav_direction = 3

			# Pareil pour l'ordonnée
			else:
				if objective.y - self.y > 0:
					fav_direction = 2

				else:
					fav_direction = 0

			# On se déplace aléatoirement avec la direction prioritaire
			self.random_direction(square, fav_direction)

	def backtracking(self, square, objective, direction, lane=[], square_range=0):
		"""
		backtracking(Square square, Square objective, int direction, list lane, int square_range) --> int
		Tente de trouver un chemin de square vers objective par backtracking
		direction : direction actuelle
		lane : coordonnées des cases déja parcourues
		square_range : longueur du chemin
		"""
		

		# Si la case actuelle correspond à la case visée, l'objectif est atteint
		if (square.x, square.y) == (objective.x, objective.y):
			return direction

		elif square_range > 15: # Si la longueur du chemin excède 15, on laisse tomber (performance)
			return -1

		else:
			# Directions disponibles
			empty_adj_squares = square.empty_adj_squares(direction)

			# On parcourt les directions disponibles
			for new_dir in empty_adj_squares:
				# Case adjacente dans la direction
				next_square = square.adjacent_square(new_dir)

				# Si on se retrouve sur une case déjà parcourue, on abandonne (boucle)
				if (next_square.x, next_square.y) in lane:
					continue

				# Par récursivité, si le résultat est concluant, on retourne la direction qui a fonctionné
				elif self.backtracking(next_square, objective, new_dir, list(lane) + [(next_square.x, next_square.y)], square_range + 1) >= 0:
					return new_dir

			return -1



	def stop(self, time):
		"""
		stop(int time) --> None
		Met le fantôme en pause pour une certaine durée
		"""
		self.pause = time

class Blinky(Ghost):
	"""
	Fantôme qui se dirige de manière aléatoire
	"""
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "blinky"
		self.points = 800

		self.load_picture()

	def set_direction(self, square):
		"""
		set_direction(Square square)
		Définit la direction du fantôme
		"""
		self.random_direction(square)

class Pinky(Ghost):
	"""
	Fantôme qui tente de poursuivre pacman dès que celui-ci est assez proche
	"""
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "pinky"
		self.points = 200
		

		self.load_picture()

	def set_direction(self, square):
		"""
		set_direction(Square square)
		Définit la direction du fantôme
		"""
		pacman = self.level.get_pacman_square()

		# Si pacman est suffisamment proche
		if self.distance_from(square, pacman) < self.level.distance:
			self.get_to_square(square, pacman)

		else:
			self.random_direction(square)


class Clyde(Ghost):
	"""
	Fantome qui tente de couper la route à pacman
	"""
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "clyde"
		self.points = 400

		self.load_picture()

	def set_direction(self, square):
		"""
		set_direction(Square square)
		Définit la direction du fantôme
		"""
		pacman = self.level.get_pacman_square()

		# Si clyde va dans la direction opposée à pacman
		# et que celui-ci est suffisamment proche, clyde tente de l'attrapper
		p_direction = self.level.pacman.direction
		distance = self.distance_from(square, pacman)

		if not p_direction == self.direction and distance < 5:
			self.get_to_square(square, pacman)
			
		else:
			# Sinon, clyde tente d'anticiper le déplacement de pacman
			# et de lui couper la route
		 	forward_square = self.find_forward_square(square, distance)

		 	# Si une case a été trouvée et que celle-ci n'est pas trop loin
		 	if forward_square and self.distance_from(square, forward_square) < self.level.distance + 5:
		 		self.get_to_square(square, forward_square)

		 	# S'il n'est pas possible de couper la route, le mouvement se fait aléatoirement
		 	else:
		 		self.random_direction(square)


	def find_forward_square(self, square, distance):
		"""
		find_forward_square(Square square, int distance)
		Tente d'anticiper le mouvement de pacman
		"""
		# Clyde tente d'atteindre une case située 5 cases en avant de pacman.
		# Valeurs de l'abscisse et de l'ordonnée à ajouter à la case de pacman
		x_forward = DIRECTIONS[self.level.pacman.direction][0] * distance
		y_forward = DIRECTIONS[self.level.pacman.direction][1] * distance

		# Case située 5 cases en avant de pacman
		square_forward = self.level.get_pacman_square() + (x_forward, y_forward)
		
		# On vérifie que la case existe (elle peut être en dehors de la grille)
		if square_forward:
			# Si la case est un mur, on essaie avec les cases d'à côté
			for plus_x in [0, -1, 1]:
				for plus_y in [0, -1, 1]:
					square_to_reach = square_forward + (plus_x, plus_y)

					if square_to_reach and square_to_reach.is_empty:
						return square_to_reach

		return None



class Inky(Ghost):
	"""
	Fantôme essayant d'aller le plus loin possible de pacman
	"""
	def __init__(self, *args, **kwargs):
		Ghost.__init__(self, *args, **kwargs)

		self.name = "inky"
		self.points = 1600

		self.load_picture()

	def set_direction(self, square):
		"""
		set_direction(Square square)
		Définit la direction du fantôme
		"""
		pacman = self.level.get_pacman_square()
		
		# Si pacman est dans la partie droite de la grille,
		# Inky va aller se cacher tout à gauche et vice versa.
		# Raisonnement analogue pour le haut/bas
		if pacman.x > 12:
			objective_x = 1
		else:
			objective_x = N_SQUARES_X - 2

		if pacman.y > 12:
			objective_y = 1
		else:
			objective_y = N_SQUARES_Y - 2

		objective = self.level.get_square(objective_x, objective_y)

		self.get_to_square(square, objective)

