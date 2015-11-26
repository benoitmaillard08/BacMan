#######################################################
#													  #
#		 BacMan : the baccalaureates Adventure		  #
#		   ---xxxxxxxxxxxxxxxxxxxxxxxxxxx---		  #
#													  #
#						Créé par					  #
#	     Benoît Léo Maillard & Mikaël Ruffieux		  #
#						 -----						  #
#					   version 0.1					  #
#					              #
#######################################################

"""
Fichier principal

Fichiers annexes : animation.py, constantes.py, data.py, graphics.py,
				   levels.py, menus.py, process.py, README.md, levels (folder).
"""

import pygame
import process
import menus

class BacMan: # Classe principale du jeu
	def __init__(self):
		pass
	
class Game: # Classe servant à gérer une partie
	def __init__(self):
		self.n_level = 0


		#### Code provisoire
		pygame.init()

		self.window = pygame.display.set_mode((800, 800))

		b = menus.Button(self.window, "Test", (10, 10), None, None)
		b.button_display()
		b.text_display()

		self.next_level()

		continuer = True

		#Boucle infinie
		while continuer:
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == pygame.locals.QUIT:     #Si un de ces événements est de type QUIT
					continuer = False      #On arrête la boucle


		#### Fin du code provisoire


	def next_level(self):
		self.n_level += 1
		self.level = process.Level(self.n_level, self.window)
