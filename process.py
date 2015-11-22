import pygame
import constantes
import parse
from shortcuts import *

""" Gestion du processus 'In Game' du jeu >BacMan the baccalaureates Adventure!< """

class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, n_level, window):

		self.n_level = n_level # Numéro du level
		self.window = window

		parse_level = parse.ParseLevel(self) # Parsing du fichier de niveau
		# Récupération de la structure du niveau sous forme de liste à deux dimensions
		self.structure = parse_level.get_structure()

		self.prepare_walls() # Préparaion de l'affichage des différentes textures de murs
		

		self.pacman = None
		self.monsters = []

		self.render()


	def render(self):
		"""Réalise le rendu graphique de tous les éléments du jeu"""
		for line in self.structure :
			for square in line:
				square.render()

		### Rendu des personnages ici

		pygame.display.flip() # Rafraichissement du rendu

	def get_square(self, x, y):
		if 0 <= y < len(self.structure):
			if 0 <= x < len(self.structure[y]):
				return self.structure[y][x]

	def prepare_walls(self):
		for line in self.structure:
			for square in line:
				if not square.is_empty:
					# Choix de la texture par rapports aux murs adjacents
					square.select_picture()


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