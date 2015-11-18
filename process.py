import levels
import pygame
import constantes
from shortcuts import *

""" Gestion du processus 'In Game' du jeu >BacMan the baccalaureates Adventure!< """

# class Game:
# 	def __init__(self):
# 		self.game_running = False # Indique que la boucle n'est pas encore lancée
# 		self.window_opened = True

# 		pygame.init()

# 		width = constantes.N_SQUARES_X * 16 * 2
# 		height = constantes.N_SQUARES_Y * 16 * 2

# 		window = pygame.display.set_mode((width, height))

# 		self.start()


########################
# Classes pour les cases
########################

class Square:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class StandardSquare(Square):
	def __init__(self, x, y, level):
		Square.__init__(self)
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
	def __init__(self, x, y):
		Square.__init__(self)
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
		if level > len(BonusPill.TYPES):
			level = 7

		# Sélection du tuple image - points par rapport au niveau
		bonus_type = BonusPill.TYPES[level-1]

		self.picture = load_terrain("fruit {}".format(bons_type[0]))
		self.points = bonus_type[1]

######################
#                    #
######################

class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, n_level):

		self.n_level = n_level
		self.structure = []

		

		self.pacman = None

		self.monsters = []


	def render(self):
		"""Réalise le rendu graphique de tous les éléments du jeu"""
		for line in self.structure :
			for square in line:
				square.render()

		### Rendu des personnages ici


# class GameLoop:
# 	def __init__(self, master):
# 		self.window_opened = True
# 		self.game_running = False
# 		self.master = master

# 	def run_loop(self):
# 		while self.window_opened:
# 			if self.game_running:
# 				# le jeu tourne

# 			# Check pour la fermeture
# 			for event in pygame.event.get():
# 				if event.type == pygame.QUIT:
# 					self.window_opened = False

# 	def pause_game(self):
# 		self.game_running = False

# 	def start_game(self):
# 		self.game_running = True

##############################
# Classes pour les personnages
##############################

Game()

