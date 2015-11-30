""" Gestion des menus du jeu >BacMan the baccalaureates Adventure!< """

# Importation des différents fichiers
import pygame
from pygame.locals import *
import constantes
import loop

class Menu:
    """
        Classe créant les différents menus du jeu
    """

    def __init__(self, window, loop):
        self.loop = loop
        self.window = window

        self.background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()

        self.container = Container(self.window, self.loop)

        self.window.blit(self.background,(0,0))

        self.content() # Ajout du contenu

        self.render() # Rendu du fonds
        self.container.calculate_coords() # Calcul et rendu des éléments

class MainMenu(Menu):
    def __init__(self, window, loop):
        Menu.__init__(self, window, loop)

        self.loop.run_loop()

    def content(self):

        # Widgets de la page
        self.container.add_button("Connexion", self.next_page(LoginPage))
        self.container.add_button("Inscription", self.next_page(RegisterPage))
        self.container.add_button("Top Scores", self.next_page(HighscoresPage))
        self.container.add_button("Quitter", self.loop.close_window)

    def next_page(self, page):
        self.loop.clear() # Suppression des boutons etc de la boucle

        page(self.loop, self.window) # Instanciation de la page


class RulesPage(MainMenu):
    """
    Classe permettant la création de la page informant le joueur sur les règles du jeu.
    """

    def __init__(self, window, loop):
        Menu.__init__(self, window, loop)

        self.background = pygame.image.load(constantes.PATH_PIC_PAGES)
        pygame.display.set_caption(caption)

        ### Définir le contenu


    def display(self):
        """
        Affichage du texte sur le fond
        """
        text_to_display = open(constantes.RULES_TEXT, 'r').read().split('\n')
        line = 300  #Ligne de départ en pixel

        #Chargement du titre
        font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.MENUFONT_SIZE)
        size = font.size(constantes.RULES_TITLE)[0]
        title = font.render(constantes.RULES_TITLE, 0, constantes.RGB_WHITE)
        self.window.blit(title, ((constantes.COTE_FOND//2 - size//2), 225))
        

        # Chargement de la police et de sa taille
        font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)

        for elt in text_to_display: # Pour chaque ligne de texte, on crée un nouvel objet text.

            font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)
            size = font.size(elt)[0] # Pour centrer le texte
            text = font.render(elt, 0, constantes.RGB_WHITE)
            
            self.window.blit(text, ((constantes.COTE_FOND//2 - size//2), line)) # 'Collage' de la ligne, avec 25 pixels de marge à gauche
            line += constantes.TEXTFONT_SIZE + 10  #La position de la prochaine ligne est placée à 25 + 10 pixels plus bas

        # Instanciation du bouton

        container = Container(self.window, self.loop)
        container.add_button('Retour', MainMenu.mainmenu())
        
        pygame.display.flip()





class CtrlsPage(RulesPage):
    """
    Classe créant la page d'explication des contrôles du jeu
    """
    def __init__(self, window, loop):
        Menu.__init__(self, window, loop)

    def display(self):
        """
        Affichage du texte et des images expliquant les contrôles du jeu.
        """
        #Chargement et placement du titre
        font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.MENUFONT_SIZE)
        size = font.size(constantes.RULES_TITLE)[0]
        title = font.render(constantes.RULES_TITLE, 0, constantes.RGB_WHITE)
        self.window.blit(title, ((constantes.COTE_FOND//2 - size//2), 225))

        #Chargement et placement des zones de textes
        font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)
        size = []
        line = 325 #Coordonnée Y de la première ligne
        i = 0
        for elt in constantes.CTRLS_TEXT: 

            size.append(font.size(elt)[0]) # Enregistrement des tailles des zones de texte dans la liste <size>
            render = font.render(elt, 0, constantes.RGB_WHITE) # Rendu du texte à ses coordonnées
            self.window.blit(render, (constantes.COTE_FOND//2 - size[i], line))

            # Chargement et placement des images
            pic = pygame.image.load(constantes.CTRLS_PIC_DIR[i]).convert_alpha()
            self.window.blit(pic,(constantes.COTE_FOND//2+84-pic.get_rect()[2]//2, line-(pic.get_rect()[3]//3))) # Placé de façon à être à la même hauteur que le texte
            line += 100                             #/\ se place par rapport à la largeur de la plus grosse image
            i += 1

        pygame.display.flip()



    

class RegisterPage(RulesPage): #Nécessite l'utilisation de Tkinter
    """
    Classe créant la page permettant à un nouveau joueur de créer un nouveau profil.
    """
    def __init__(self, window, loop):
        Menu.__init__(self, window, loop)

        
        
        




class LoginPage(SignUpPage): #Nécessite l'utilisation de Tkinter
    """
    Classe créant la page permettant à un joueur existant de se logger.
    """
    def __init__(self, window, loop):
        Menu.__init__(self, window, loop)
        


        

class HighscoresPage:
    """
    Classe créant la page affichant les highscores du jeu ET du joueur s'il est loggé.
    """
    def __init__(self, window, loop):
        Menu.__init__(self, window, loop)

        ### Elements ici