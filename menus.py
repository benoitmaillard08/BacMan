""" Gestion des menus du jeu >BacMan the baccalaureates Adventure!< """

# Importation des différents fichiers
import pygame
from pygame.locals import *
import constantes
import loop

class MainMenu:
    """
        Classe créant les différents menus du jeu
    """

    def __init__(self, window, loop):
        pygame.init()

        self.loop = loop
        self.window = window


    def mainmenu(self):
        """
        Méthode créant le menu principal
        """
        # Importation des images
        # Menu
        background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
        self.window.blit(background,(0,0))

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
    def __init__(self, caption='Rules Page', window, loop):
        """
        Méthode créant la page.
        """
        pygame.init()

        self.window = window
        self.loop = loop

        pygame.display.set_caption(caption)

        #Chargement du fond
        background = pygame.image.load(constantes.PATH_PIC_PAGES)
        self.window.blit(background, (0,0))

        #Mise à jour de la page
        pygame.display.flip()


        ##### MANQUE LE GESTIONNAIRE D'EVENEMENTS   ###########

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
    def __init__(self):
        RulesPage.__init__(self, 'Controles Page')

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



    

class SignUpPage(RulesPage): #Nécessite l'utilisation de Tkinter
    """
    Classe créant la page permettant à un nouveau joueur de créer un nouveau profil.
    """
    def __init__(self, title='Sign-Up Page'):
        """
        __init__(str title) --> None. On peut modifier le nom de la page.
        Initialisation d'une fenêtre Tkinter pour la gestion de l'enregistrement de nouveaux joueurs.
        """
##        self.window = Tk()   # Création de la fenêtre
##
##        self.window.title(title) #Titre de la page
##
##        # Chargement du fond
##        background = Canvas(self.window, width=constantes.COTE_FOND, height=constantes.COTE_FOND, background='black')
##
##        pic = PhotoImage(file=constantes.PATH_PIC_PAGES)
##        background.create_image(0,0,anchor=NW,image=pic)
##
##        background.pack()
##
##        self.window.mainloop()

        
        
        




class LoginPage(SignUpPage): #Nécessite l'utilisation de Tkinter
    """
    Classe créant la page permettant à un joueur existant de se logger.
    """
    def __init__(self):
        SignUpPage.__init__(self, 'Login Page')

    def login_display(self):
        """
        nick = StringVar()
        entry = Entry(self.window, width=30)
        entry.pack()
        label = Label(self.window, text= 'test', bg='yellow')
        label.pack()
        """
        


        

class HighscoresPage:
    """
    Classe créant la page affichant les highscores du jeu ET du joueur s'il est loggé.
    """
    pygame.init()
    pass


class Container:
    MARGIN = 10
    """
    Classe créant un conteneur de boutons pour que ceux-ci soient centrés horizontalement et verticalement
    """

    def __init__(self, window, loop):
        self.window = window
        self.loop = loop

        self.l_buttons = []

        self.button_picture = pygame.image.load(constantes.PATH_PIC_BUTTON)

    def add_button(self, text, callback):
        button = Button(self.window, text, callback, self.loop)

        self.l_buttons.append(button)

    def calculate_coords(self):
        # Hauteur nécessaire pour un bouton et les marges autour du bouton
        button_height = self.button_picture.get_height() + 2 * Container.MARGIN

        # Hauteur de la pile de boutons avec les marges
        total_height = button_height * len(self.l_buttons)

        # Coordonné y du coin supérieur gauche du premier bouton
        coord_y = (self.window.get_height() - total_height) / 2

        # Coordonné x du coin supérieur gauche de tous les boutons
        coord_x = (self.window.get_width() - self.button_picture.get_width()) / 2

        for button in self.l_buttons:
            button.set_coords(coord_x, coord_y + Container.MARGIN)
            coord_y += button_height

            button.render()


class Button:
    """
    Classe d'instenciation des boutons
    """
    def __init__(self, window, text, callback, loop):
        """
        __init__() --> None.
        """

        self.coords = (0, 0)

        self.text = text
        self.window = window    # variable 'background' de la classe 'MainMenu'
        self.action = callback # fonction à exécuter lors du clic sur le bouton
        self.loop = loop

        self.button_surface = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()

        # Ajout du bouton dans la boucle pour que celle-ci détecte les clics sur le bouton
        self.loop.add_button(self)

    def render(self):

        # Positionnement du bouton dans la fenêtre
        self.window.blit(self.button_surface, self.coords)

        # Chargement de la police + taille de la police
        font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.MENUFONT_SIZE)
        self.text_surface = font.render(self.text, 0, constantes.RGB_WHITE)

        # Raccourcis
        b = self.button_surface
        t = self.text_surface

        #Affichage du texte en fonction de sa taille et celle du bouton, afin qu'il soit centré quelque soit sa taille
        self.window.blit(self.text_surface, (
            (self.coords[0] + b.get_width() / 2) - t.get_width() / 2,
            (self.coords[1] + b.get_height() / 2) - t.get_height() / 2
        ))

    def set_coords(self, x, y):
        self.coords = (x, y)

    def check_coords(self, coords):
        if self.coords[0] < coords[0] < self.coords[0] + self.button_surface.get_width():
            if self.coords[1] < coords[1] < self.coords[1] + self.button_surface.get_height():
                return True

        return False

    def disable(self):
        pass

    def enable(self):
        pass
