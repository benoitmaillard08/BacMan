""" Gestion des menus du jeu >BacMan the baccalaureates Adventure!< """

# Importation des différents fichiers
import pygame
import process
from pygame.locals import *
import constantes
import loop
from widget import *
import database


class Menu:
    """
        Classe créant les différents menus du jeu
    """

    def __init__(self, window, loop):
        self.loop = loop
        self.window = window

        self.background = pygame.image.load(constantes.PATH_PIC_PAGES).convert()

        self.container = Container(self, self.loop)

        self.loop.page = self

        # Marges du conteneur
        self.margin_top = 200
        self.margin_bottom = 100

        self.loop.clear()
        self.content() # Définition du contenu

        # Affichage du contenu du conteneur
        self.container.set_margin(self.margin_top, self.margin_bottom)
        self.container.calculate_coords()

        # Lancement de la boucle d'évènement si celle-ci est arrêtée
        if not self.loop.loop_running:
            self.loop.run_loop()

    def next_page(self, page):
        self.loop.clear() # Suppression des boutons etc de la boucle

        page(self.window, self.loop) # Instanciation de la page

    def render(self):
        if self.background:
            self.window.blit(self.background,(0,0)) # Rendu du fonds

        self.container.render()

class MainMenu(Menu):
    def content(self):
        # Changement du fond
        self.background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
        
        # Marges du haut et du bas pour le conteneur (espace occupé par des éléments du fonds)
        self.margin_top = 260
        self.margin_bottom = 100

        # Widgets de la page
        self.container.add_widget(Button(self, self.loop, "Connexion", lambda: self.next_page(LoginPage)))
        self.container.add_widget(Button(self, self.loop, "Inscription", lambda: self.next_page(RegisterPage)))
        self.container.add_widget(Button(self, self.loop, "Top Scores", lambda: self.next_page(HighscoresPage)))
        self.container.add_widget(Button(self, self.loop, "Quitter", self.loop.close_window))
        self.container.add_widget(Button(self, self.loop, "Jeu direct", lambda: self.next_page(GameMenu))) #Bouton momentané

class LoginPage(Menu):
    """
    Classe créant la page permettant à un joueur existant de se logger.
    """

    def content(self):
        self.pseudo = self.container.add_widget(TextInput(self, self.loop, "Pseudo", None))
        self.password = self.container.add_widget(TextInput(self, self.loop, "Password", None))
        self.container.add_widget(Button(self, self.loop, "Entrer", lambda : LoginPage.test(self)))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))

    # def test(self, onRegisterPage=False):

    #     tested_infos = database.Register(self.pseudo.content, self.password.content).test_infos(onRegisterPage)

    #     if  tested_infos == 'Logged':
    #         # + message <Pseudo! Nous attendions ton retour ...>
    #         self.next_page(GameMenu)

    #     elif tested_infos == 'NotRegistered' and onRegisterPage == False:   # Test si l'utilisateur est déjà sur la page pour s'enregistrer
    #         self.next_page(RegisterPage)
    #         # + message <Veuillez vous enregistrer d'abord!>

    #     elif tested_infos == 'NewRegistered':
    #         self.next_page(GameMenu)
    #         # + message <Bienvenue Pseudo!>
    #     elif tested_infos == 'TakenPassword':
    #         # message d'alerte <Pseudo déjà utilisé>
    #         pass

    #     else:
    #         # Message d'erreur <Mauvais MdP!>
    #         pass
            

class RegisterPage(Menu):
    """
    Classe créant la page permettant à un nouveau joueur de créer un nouveau profil.
    """
    def content(self):

        self.pseudo = self.container.add_widget(TextInput(self, self.loop, "Pseudo", None))
        self.password = self.container.add_widget(TextInput(self, self.loop, "Password", None))
        self.container.add_widget(Button(self, self.loop, "Entrer", lambda : LoginPage.test(self, onRegisterPage=True)))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))

class GameMenu(Menu):
    def content(self):
        self.container.add_widget(Button(self, self.loop, "Jouer", self.launch_game))
        self.container.add_widget(Button(self, self.loop, "Controles", lambda: self.next_page(CtrlsPage)))
        self.container.add_widget(Button(self, self.loop, "Regles", lambda: self.next_page(RulesPage)))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))

    def launch_game(self):
        # self.loop.clear() # Suppression des boutons etc de la boucle
        game = process.Game(self.window, self.loop)


class RulesPage(Menu):
    def content(self):
        rules_text = open(constantes.RULES_TEXT, 'r').read()

        self.container.add_widget(TextDisplay(self, self.loop, rules_text))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(GameMenu)))


class CtrlsPage(Menu):
    """
    Classe créant la page d'explication des contrôles du jeu
    """
    def content(self):
        controls_text = open(constantes.CTRLS_TEXT, 'r').read()

        self.container.add_widget(TextDisplay(self, self.loop, controls_text))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(GameMenu)))

    # def display(self):
    #     """
    #     Affichage du texte et des images expliquant les contrôles du jeu.
    #     """
    #     #Chargement et placement du titre
    #     font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.MENUFONT_SIZE)
    #     size = font.size(constantes.RULES_TITLE)[0]
    #     title = font.render(constantes.RULES_TITLE, 0, constantes.RGB_WHITE)
    #     self.window.blit(title, ((self.window.get_width()//2 - size//2), 225))

    #     #Chargement et placement des zones de textes
    #     font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)
    #     size = []
    #     line = 325 #Coordonnée Y de la première ligne
    #     i = 0
    #     for elt in constantes.CTRLS_TEXT: 

    #         size.append(font.size(elt)[0]) # Enregistrement des tailles des zones de texte dans la liste <size>
    #         render = font.render(elt, 0, constantes.RGB_WHITE) # Rendu du texte à ses coordonnées
    #         self.window.blit(render, (self.window.get_width()//2 - size[i], line))

    #         # Chargement et placement des images
    #         pic = pygame.image.load(constantes.CTRLS_PIC_DIR[i]).convert_alpha()
    #         self.window.blit(pic,(self.window.get_width()//2+84-pic.get_rect()[2]//2, line-(pic.get_rect()[3]//3))) # Placé de façon à être à la même hauteur que le texte
    #         line += 100                             #/\ se place par rapport à la largeur de la plus grosse image
    #         i += 1


class HighscoresPage(Menu):
    """
    Classe créant la page affichant les highscores du jeu ET du joueur s'il est loggé.
    """
    def content(self):
        self.container.add_widget(TextDisplay(self, self.loop, "En cours de développement"))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))


class InGameMenu(Menu):
    def __init__(self, window, loop, game):
        self.game = game
        Menu.__init__(self, window, loop)

    def content(self):
        self.margin_top = 672
        self.margin_bottom = 0

        self.score = self.container.add_widget(TextDisplay(self, self.loop, "Score : {}".format(self.game.score)))
        self.lives = self.container.add_widget(TextDisplay(self, self.loop, "Vies restantes : {}".format(self.game.lives)))

        self.background = None

    def update_score(self):
        self.score.text = "Score : {}".format(self.game.score)
        self.score.update_text()

    def update_lives(self):
        self.lives.text = "Vies restantes : {}".format(self.game.lives)
        self.lives.update_text()


class NextLevelMenu(Menu):
    def __init__(self, window, loop, game):
        self.game = game

        Menu.__init__(self, window, loop)

    def content(self):
        self.container.add_widget(TextDisplay(self, self.loop, "Bravo ! Vous avez réussi le niveau {}".format(self.game.level.n_level)))
        self.container.add_widget(Button(self, self.loop, "Continuer", self.game.next_level))

class EndGameMenu(Menu):
    def __init__(self, window, loop, game):
        self.game = game

        Menu.__init__(self, window, loop)

    def content(self):
        text = """Jeu terminé !
Vous avez obtenu le score de {} points
et atteint le niveau {}""".format(self.game.score, self.game.level.n_level)
        self.container.add_widget(TextDisplay(self, self.loop, text))
        self.container.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(GameMenu)))