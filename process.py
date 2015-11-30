import pygame
from constantes import *
import parse
from shortcuts import *
import time

""" Gestion du processus 'In Game' du jeu >BacMan the baccalaureates Adventure!< """

class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, n_level, window, loop):

		self.n_level = n_level # Numéro du level
		self.window = window
		self.background = pygame.image.load(GAME_BACKGROUND)

		parse_level = parse.ParseLevel(self) # Parsing du fichier de niveau

		# Récupération de la structure du niveau ainsi que les personnages
		self.structure = parse_level.get_structure()
		self.pacman = parse_level.get_pacman()
		self.ghosts = parse_level.get_ghosts()

		self.prepare_walls() # Préparation de l'affichage des différentes textures de murs

		self.render()

		# On signale à la boucle qu'il faut gérer les animation et les évènements
		# qui se rapportent au niveau
		loop.level = self

		self.pause = False # Indique si le jeu est en pause


	def render(self):
		"""Réalise le rendu graphique de tous les éléments du jeu"""

		self.window.blit(self.background, (0, 0))
		
		for line in self.structure :
			for square in line:
				square.render()

		self.pacman.render()

		for g in self.ghosts:
			g.render()

		### Rendu des personnages ici

		

	def get_square(self, x, y):
		if 0 <= y < len(self.structure):
			if 0 <= x < len(self.structure[int(y)]):
				return self.structure[int(y)][int(x)]

	def prepare_walls(self):
		for line in self.structure:
			for square in line:
				if not square.is_empty:
					# Choix de la texture par rapports aux murs adjacents
					square.select_picture()

	def game_tic(self):
		if not self.pause:
			for ghost in self.ghosts:
				ghost.move()

			self.pacman.move()


			self.render()