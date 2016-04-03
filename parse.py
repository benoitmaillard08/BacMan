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
		"""
		Parsing du code du niveau
		"""

		y = 0 

		# Coordonnées des points de téléportation
		tp_coords = {}

		for line in self.file_lines:
			level_line = [] # Ligne du niveau
			self.structure.append(level_line)

			x = 0

			for char in line:
				if char == WALL:
					square = entities.Wall(self.level_ref, x, y)

				elif char == GHOST_DOOR:
					square = entities.GhostDoor(self.level_ref, x, y)

				else:
					# S'il ne s'agit pas d'un mur, on instancie une case standard
					square = entities.StandardSquare(self.level_ref, x, y)

					# S'il s'agit d'une pastille
					if char in self.pills:
						square.add_pill(self.pills[char])
						self.level_ref.n_pills += 1

					# S'il s'agit d'un personnage (pacman/fantômes)
					elif char in self.chars:
						self.chars[char].set_coords(x, y)

					# Gestion des points de téléportation
					# Deux numéros identiques indiquent un lien de téléportation
					elif char in "0123456789":
						# S'il s'agit du deuxième point
						if char in tp_coords:
							# L'élément du dictionnaire avec le numéro en clé correspond aux coordonnées
							# de l'autre point à relier
							square.add_tp_coords(*tp_coords[char])
							self.structure[tp_coords[char][1]][tp_coords[char][0]].add_tp_coords(x, y)

						# S'il s'agit du premier point, les coordonnées sont placés dans le dictionnaire
						else:
							tp_coords[char] = (x, y)

					else:
						### Caractère inconnu : erreur
						pass

				x += 1
				level_line.append(square) # La ligne est ajoutée

			y += 1

	def get_structure(self):
		"""
		Retourne la liste à deux dimensions correspondant aux cases du niveau
		"""
		return self.structure

	def get_pacman(self):
		"""
		Retourne l'objet PacMan
		"""
		return self.chars[PACMAN]

	def get_ghosts(self):
		"""
		Retourne les objets fantômes
		"""
		ghosts = [
			self.chars[BLINKY],
			self.chars[PINKY],
			self.chars[CLYDE],
			self.chars[INKY],
		]

		return ghosts