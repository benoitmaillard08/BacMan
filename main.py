#######################################################
#													  #
#		 BacMan : the baccalaureates Adventure		  #
#		   ---xxxxxxxxxxxxxxxxxxxxxxxxxxx---		  #
#													  #
#						Créé par					  #
#	     Benoît Léo Maillard & Mikaël Ruffieux		  #
#						 -----						  #
#					   version 0.1					  #
#													  #
#######################################################

"""
Fichier principal

Fichiers annexes : animation.py, constantes.py, data.py, graphics.py,
				   levels.py, menus.py, process.py, README.md, levels (folder).
"""

import pygame
import process

class BacMan: # Classe principale du jeu
	def __init__(self):
		pass
	
class Game: # Classe servant à gérer une partie
	def __init__(self):
		self.n_level = 0

	def next_level(self, n_level):
		self.n_level += 1
		self.level = process.Level(self.n_level)