""" Classes permettant la gestion et génération des niveaux du Jeu >BacMan the baccalaureates Adventure!< """

# Importation du module pygame et du fichier contenant les constantes du jeu

import pygame
from pygame.locals import *
from constantes import *
import entities

class ParseLevel:
	def __init__(self, level):
		self.level_ref = level
		self.level_filename = LEVELS_DIR + FILENAME_PATTERN.format(level.n_level)

		# Initiation des entités du niveau
		self.structure = []

		self.chars = {
		 	PACMAN : entities.PacMan(level),
		 	BLINKY : entities.Blinky(level),
		 	PINKY : entities.Pinky(level),
		 	CLYDE : entities.Clyde(level),
		 	INKY : entities.Inky(level),
		}


		self.pills = {
			# L'argument level correspond à la référence
			# de l'instance de la classe Level
			# Les clés du dictionnaire sont les symboles utilisés
			# dans les .level et définis dans constantes.py
			PILL : entities.StandardPill(level),
			POWER_PILL : entities.PowerPill(level),
			BONUS_PILL : entities.BonusPill(level),
		}

		# Ouverture du fichier et lecture du contenu
		level_file = open(self.level_filename, 'r')
		content = level_file.read()

		# Liste des lignes du fichier
		self.file_lines = content.split("\n")

		self.parse()

	def parse(self):

		y = 0

		for line in self.file_lines:
			level_line = [] # Ligne du niveau
			x = 0

			for char in line:
				if char == WALL:
					square = entities.Wall(self.level_ref, x, y)

				else:
					square = entities.StandardSquare(self.level_ref, x, y)

					if char in self.pills:
						square.add_pill(self.pills[char])
						self.level_ref.n_pills += 1

					elif char in self.chars:
						self.chars[char].set_coords(x, y)
					else:
						### Caractère inconnu : erreur
						pass

				x += 1
				level_line.append(square)

			y += 1
			self.structure.append(level_line)

	def get_structure(self):
		return self.structure

	def get_pacman(self):
		return self.chars[PACMAN]

	def get_ghosts(self):
		ghosts = [
			self.chars[BLINKY],
			self.chars[PINKY],
			self.chars[CLYDE],
			self.chars[INKY],
		]

		return ghosts