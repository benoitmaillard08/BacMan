import levels
import pygame
import constantes
import parse
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

######################
#                    #
######################

class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, n_level):

		self.n_level = n_level

		parse_level = parse.ParseLevel(self)

		self.structure = parse_level.get_structure()
		

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

