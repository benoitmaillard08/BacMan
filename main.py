#######################################################
#                                                     #
#        BacMan : the baccalaureates Adventure        #
#          ---xxxxxxxxxxxxxxxxxxxxxxxxxxx---          #
#                                                     #
#                       Créé par                      #
#        Benoît Léo Maillard & Mikaël Ruffieux        #
#                        -----                        #
#                      version 0.1                    #
#                                                     #
#######################################################

"""
Fichier principal

Fichiers annexes : animation.py, constantes.py, data.py, graphics.py,
                   levels.py, menus.py, process.py, README.md, levels (folder).
"""

import pygame
import process
import menus
from constantes import *
import loop

class BacMan: # Classe principale du jeu
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        pygame.display.set_caption("Bacman : the baccalaureates Adventure")
        self.loop = loop.Loop()

        self.main_menu = menus.MainMenu(self.window, self.loop)
    
class Game: # Classe servant à gérer une partie
    def __init__(self):
        self.n_level = 0

        #### Code provisoire
        pygame.init()

        self.window = pygame.display.set_mode((800, 800))

        self.loop = loop.Loop()


        # c = menus.Container(self.window, loop)
        # c.add_button("Test 1", lambda: print("Bouton 1"))
        # c.add_button("Test 2", lambda: print("Bouton 2"))
        # c.add_button("Test 3", lambda: print("Bouton 3"))
        # c.add_button("HAHAHAHAHA", None)

        # c.calculate_coords()

        self.next_level()

        # pygame.display.flip()

        self.loop.run_loop()


        #### Fin du code provisoire


    def next_level(self):
        self.n_level += 1
        self.level = process.Level(self.n_level, self.window, self.loop)

BacMan()
