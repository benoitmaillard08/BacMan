""" Gestion des menus du jeu >BacMan the baccalaureates Adventure!< """

# Importation de pygame et des constantes
import pygame
from pygame.locals import *
import constantes

class MainMenu:
    """
        Classe créant les différents menus du jeu
    """

    def __init__(self):
        pygame.init()

    def mainmenu(self):
        """
        Méthode créant le menu principal
        """
        # Création de la fenêtre
        window = pygame.display.set_mode((constantes.COTE_FOND, constantes.COTE_FOND), RESIZABLE)

        # Importation des images
        # Menu
        background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
        window.blit(background,(0,0))

        #---------------

        # Rafrachissement de l'écran
        pygame.display.flip()

        #Gestionnaire d'événements
        flag = 1

        while flag:
            for event in pygame.event.get():    # Parcours la liste des éléments reçus
                if event.type == QUIT:
                    flag = 0
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x = event.pos[0]    #Les positions du clic de la souris sont enregistrés pour être analyser
                    y = event.pos[1]




        # Sortie de la boucle et fermeture de la fenêtre
        pygame.display.quit()

    def mouse_position(self, pos_x, pos_y):
        """
        mouse_position(int pos_x, int pos_y) --> None.

        On entre les positions de la souris dans la méthode, et celle-ci analysera sa position, pour éventuellement
        lancer la méthode du bouton activé.
        """
        x = pos_x
        y = pos_y


class RulesPage:
    """
    Classe permettant la création de la page informant le joueur sur les règles du jeu.
    """
    def __init__(self):
        """
        Méthode créant la page.
        """
        pygame.init()

        window = pygame.display.set_mode((constantes.COTE_FOND, constantes.COTE_FOND), RESIZABLE)

        #Chargement du fond
        background = pygame.image.load(constantes.PATH_PIC_PAGES)
        window.blit(background, (0,0))

        #Chargement du titre
        font = pygame.font.Font((constantes.FONT_PATH, constantes.FONT_SIZE)
        title = font.render(constantes.RULES_TITLE, 0, constantes.RGB_WHITE)
        window.blit(title, (10,10)) # Chargement dans la fenêtre aux positions p.e. (10,10)

        #Chargement du texte
        rules = font.render(constantes.RULES_TEXT, 0, constantes.RGB_WHITE)
        window.blit(rules, (20,10))

        #Mise à jour de la page
        window.display.flip()


        ##### MANQUE LE GESTIONNAIRE D'EVENEMENTS   ###########



class Button:
    """
    Classe d'instenciation des boutons
    """
    def __init__(self, master, text_str, coords, event_handler, callback):
        """
        __init__(event_handler, str text_str, tup coords, callback) --> None.
        """
        self.coords = coords
        self.text_str = text_str
        self.master = master    # variable 'background' de la classe 'MainMenu'

    def button_display(self, coords):
        """
        button_display(str text_str, tup coords) --> None.
        """

        # Chargement de l'image
        button = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()
        self.button_size = button.get_rect()
        # Positionnement du bouton dans la fenêtre
        master.blit(button, self.coords)

    def text_display(self, text_str):
        """
        text_display(tup coords, str text_str) --> None.
        """

        # Chargement de la police + taille de la police
        font = pygame.font.Font(constantes.FONT_PATH, constantes.FONT_SIZE)
        text = font.render(text_str, 0, constantes.RGB_WHITE)

        text_size = text.get_rect() # Enregistrement de la zone de texte dans un tuple (x,y)

        #Affichage du texte en fonction de sa taille et celle du bouton, afin qu'il soit centré quelque soit sa taille
        master.blit(text,((button_size[0] - text_size[0])/2,(button_size[1] - text_size[1])/2))
