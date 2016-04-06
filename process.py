import pygame
from constantes import *
import parse
from shortcuts import *
import time
import menus

class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, master, n_level, window, loop):

		self.master = master
		self.n_level = n_level # Numéro du level
		self.window = window
		self.background = pygame.image.load(GAME_BACKGROUND)

		self.n_pills = 0 # Nombre de pillules

		parse_level = parse.ParseLevel(self) # Parsing du fichier de niveau

		# Récupération de la structure du niveau ainsi que les personnages
		self.structure = parse_level.get_structure()
		self.pacman = parse_level.get_pacman()
		self.ghosts = parse_level.get_ghosts()

		self.prepare_walls() # Préparation de l'affichage des différentes textures de murs

		# Premier rendu du niveau
		self.render()

		# On signale à la boucle qu'il faut gérer les animation et les évènements
		# qui se rapportent au niveau
		loop.level = self

		self.in_game_pause = False # Indique si le jeu est en pause
		self.delay = 0

		# Distance à partir de laquelle certains fantômes poursuivent pacman
		self.distance = n_level + 3


	def render(self):
		"""
		render() --> None
		Réalise le rendu graphique de tous les éléments du jeu
		"""

		self.window.blit(self.background, (0, 0))
		
		for line in self.structure :
			for square in line:
				square.render()

		self.pacman.render()

		for g in self.ghosts:
			g.render()

		### Rendu des personnages ici

		

	def get_square(self, x, y):
		"""
		get_square(int x, int y) --> entities.Square
		Retourne l'objet case corresondant aux coordonnées
		"""
		if 0 <= y < len(self.structure):
			if 0 <= x < len(self.structure[int(y)]):
				return self.structure[int(y)][int(x)]

		else:
			return None

	def get_pacman_square(self):
		"""
		get_pacman_square() --> entities.Square
		Retourne la case sur laquelle se trouve pacman
		"""
		x, y = int(round(self.pacman.x)), int(round(self.pacman.y))

		return self.get_square(x, y)

	def prepare_walls(self):
		"""
		prepare_walls() --> None
		Prépare le rendu des murs selons les cases adjacentes
		"""
		for line in self.structure:
			for square in line:
				if not square.is_empty:
					# Choix de la texture par rapports aux murs adjacents
					square.select_picture()

	def game_tic(self):
		"""
		game_tic() --> None
		Effectue une itération du jeu comprenant les mouvements et le rendu de chaque élément
		"""
		# Si le jeu n'est pas en pause
		if not self.master.pause:
			# Si le jeu n'est pas en pause pour un temps défini
			if not self.delay:
				# Mouvements des personnages
				for ghost in self.ghosts:
					ghost.move()

				self.pacman.move()

			else:
				# Gestion de la mise en pause temporaire
				if self.delay == 1:
					self.delay = 0

				elif self.delay:
					self.delay -= 1

		# Rendu des éléments du jeu
		self.render()

	def pause_ghosts(self):
		"""
		pause_ghosts() --> None
		Permet de mettre en pause les fantômes lorsque PM mange un pastille de puissance
		"""
		for ghost in self.ghosts:
			ghost.stop(100)

	def pause_game(self, time):
		"""
		pause_game(int time) --> None
		Permet de mettre en pause le jeu temporairement avec une durée indiquée ou non
		"""
		self.delay = time