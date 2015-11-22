""" Classes permettant la gestion et génération des niveaux du Jeu >BacMan the baccalaureates Adventure!< """

# Importation du module pygame et du fichier contenant les constantes du jeu

import pygame
from pygame.locals import *
from constantes import *
import process

class ParseLevel:
	def __init__(self, level):
		self.level_filename = constantes.FILENAME_PATTERN.format(n_level)

		self.n_level = level.n_level

		# Initiation des entités du niveau
		self.structure = []
		self.pacman = None
		self.monsters = []


		# self.chars = {
		# 	PACMAN : process.
		# }

		self.pills = {
			PILL : process.StandardPill(),
			POWER_PILL : process.PowerPill(),
			BONUS_PILL : process.BonusPill(self.n_level),
		}

		# Ouverture du fichier et lecture du contenu
		level_file = open(self.level_filename, 'r')
		content = level_file.read()

		# Liste des lignes du fichier
		self.l_lines = content.split("\n")

		self.parse()

	def parse(self):

		for y in range(self.l_lines):
			level_line = [] # Ligne du niveau

			for x in range(structure[y]):
				if char == WALL:
					square = process.Wall()

				else:
					square = process.StandardSquare()

					if char in self.squares:
						square.add_pill(self.pills[char])
					#elif char in self.chars:
					#
					#

				level_line.append(square)
			structure.append(level_line)

