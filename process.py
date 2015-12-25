import pygame
from constantes import *
import parse
from shortcuts import *
import time
import menus

""" Gestion du processus 'In Game' du jeu >BacMan the baccalaureates Adventure!< """

class Game:
	"""
	Classe permettant la gestion du déroulement de la partie
	"""
	def __init__(self, window, loop):
		self.n_level = 0

		self.lives = 3
		self.score = 0
		self.window = window
		self.loop = loop

		self.next_level() # Lancement du premier niveau

	def end_level(self):
		"""
		Prépare le message d'info à la fin du niveau
		"""

		# Menu de fin de niveau
		self.loop.page = menus.NextLevelMenu(self.window, self.loop, self)

		self.level = None

	def next_level(self):
		"""
		Passage au niveau suivant
		"""
		self.n_level += 1
		self.loop.clear()
		menus.InGameMenu(self.window, self.loop, self)
		self.level = Level(self, self.n_level, self.window, self.loop)

	def update_score(self, points):
		"""
		Mise à jour du score
		"""
		self.score += points

		self.loop.page.update_score()

	def update_lives(self):
		"""
		Mise à jour du nombre de vies
		"""
		self.lives -= 1

		self.loop.page.update_lives()

		# Lorsque les vies du joueur atteignent 0, le jeu est fini
		if self.lives == 0:	
			self.end_game()

	def end_game(self):
		"""
		Fin de la partie
		"""
		self.loop.page = menus.EndGameMenu(self.window, self.loop, self)


class Level:
	"""Classe permettant de créer un niveau"""

	def __init__(self, game, n_level, window, loop):

		self.game = game
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

		self.render()

		# On signale à la boucle qu'il faut gérer les animation et les évènements
		# qui se rapportent au niveau
		loop.level = self

		self.pause = False # Indique si le jeu est en pause
		self.delay = 0


	def render(self):
		"""Réalise le rendu graphique de tous les éléments du jeu"""
		print("ok")

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
		Retourne l'objet case corresondant aux coordonnées
		"""
		if 0 <= y < len(self.structure):
			if 0 <= x < len(self.structure[int(y)]):
				return self.structure[int(y)][int(x)]

	def prepare_walls(self):
		"""
		Prépare le rendu des murs selons les cases adjacentes
		"""
		for line in self.structure:
			for square in line:
				if not square.is_empty:
					# Choix de la texture par rapports aux murs adjacents
					square.select_picture()

	def game_tic(self):
		"""
		Effectue une itération du jeu comprenant les mouvements et le rendu de chaque élément
		"""
		if not self.pause:
			for ghost in self.ghosts:
				ghost.move()

			self.pacman.move()

		else:
			# Gestion de la mise en pause temporaire
			if self.delay == 1:
				self.delay = 0
				self.pause = False

			elif self.delay:
				self.delay -= 1

		self.render()

	def pause_ghosts(self):
		"""
		Permet de mettre en pause les fantômes lorsque PM mange un pastille de puissance
		"""
		for ghost in self.ghosts:
			ghost.stop(100)

	def pause_game(self, time=0):
		"""
		Permet de mettre en pause le jeu temporairement avec une durée indiquée ou non
		"""
		if time:
			self.delay = time
		
		self.pause = True