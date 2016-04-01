#######################################################
#                                                     #
#        BacMan : the baccalaureates Adventure        #
#          ---xxxxxxxxxxxxxxxxxxxxxxxxxxx---          #
#                                                     #
#                       Créé par                      #
#        Benoît Léo Maillard & Mikaël Ruffieux        #
#                        -----                        #
#                      version 0.8                    #
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

class BacMan:
    """
    Classe principale de l'application
    """
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        pygame.display.set_caption("Bacman : the baccalaureates Adventure")
        self.loop = loop.Loop()

        self.main_menu = menus.MainMenu(self.window, self.loop)

BacMan()
