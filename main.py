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


		c = menus.Container(self.window, None)
		c.add_button("Test 1", None)
		c.add_button("Test 2", None)
		c.add_button("Test 3", None)
		c.add_button("HAHAHAHAHA", None)

		c.calculate_coords()

		# self.next_level()

		pygame.display.flip()

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
