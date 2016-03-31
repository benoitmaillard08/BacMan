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

        self.container = Container(self, 200, 100)

        self.event_widgets = [] # Liste contenant tous les widgets liés à des évènements

        self.loop.page = self
        self.focus = None

        # Ajoute un widget pour que le pseudo du joueur apparaisse sur toutes les pages du menu
        # self.pseudo = self.add_widget(TextDisplay(self, self.loop, "Connecté en tant que {}".format(self.loop.player)))

    def next_page(self, page, *args, **kwargs):
        page(self.window, self.loop, *args, **kwargs) # Instanciation de la page

    def tic(self):
        self.render()

    def render(self):
        if self.background:
            self.window.blit(self.background,(0,0)) # Rendu du fonds

        self.container.render()

    def add_widget(self, widget):
        if widget.event:
            self.event_widgets.append(widget)

        # Tous les widgets sont ajoutés au container 
        self.container.add_widget(widget)

        return widget

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if self.focus: # Si un widget a le focus, le focus lui est retiré
                    self.focus.remove_focus()
                    self.focus = None

                for widget in self.event_widgets:
                    if widget.check_coords(event.pos): # On regarde si l'utilisateur a cliqué sur un widget
                        widget.action()
                        break

        elif event.type == pygame.KEYDOWN:
            # Si un widget a le focus sur la page
            if self.focus:
                self.focus.keydown(event)

            else:
                self.keydown(event)

    def keydown(self, event):
        pass

    def focus_on(self, widget):
        self.focus = widget

class MainMenu(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)
        # Changement du fond
        self.background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
        
        # Marges du haut et du bas pour le conteneur (espace occupé par des éléments du fonds)
        self.container.set_margin(260, 100)

        # Widgets de la page
        self.add_widget(Button(self, self.loop, "Connexion", lambda: self.next_page(LoginPage)))
        self.add_widget(Button(self, self.loop, "Inscription", lambda: self.next_page(RegisterPage)))
        self.add_widget(Button(self, self.loop, "Top Scores", lambda: self.next_page(HighscoresPage)))
        self.add_widget(Button(self, self.loop, "Quitter", self.loop.close_window))
        self.add_widget(Button(self, self.loop, "Jeu direct", lambda: self.next_page(GameMenu))) #Bouton momentané

        # Lancement de la boucle d'évènement si celle-ci n'a pas encore été lancée (ouverture du programme)
        if not self.loop.loop_running:
            self.loop.run_loop()

class LoginPage(Menu):
    """
    Classe créant la page permettant à un joueur existant de se logger.
    """

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.pseudo = self.add_widget(TextInput(self, self.loop, "Pseudo", None))
        self.password = self.add_widget(PasswordInput(self, self.loop, "Password", None))
        self.add_widget(Button(self, self.loop, "Entrer", self.test))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))

    def test(self, onRegisterPage=False):


        test = data.Register(self.pseudo.content, self.password.content).test_infos(onRegisterPage)

        if  tested_infos == 'Logged':
            # + message <Pseudo! Nous attendions ton retour ...>
            self.next_page(GameMenu)

        elif tested_infos == 'NotRegistered' and onRegisterPage == False:   # Test si l'utilisateur est déjà sur la page pour s'enregistrer
            self.next_page(RegisterPage)
            # + message <Veuillez vous enregistrer d'abord!>

        elif tested_infos == 'NewRegistered':
            self.next_page(GameMenu)
            # + message <Bienvenue Pseudo!>
        elif tested_infos == 'TakenPassword':
            # message d'alerte <Pseudo déjà utilisé>
            pass

        else:
            # Message d'erreur <Mauvais MdP!>
            pass
            

class RegisterPage(Menu):
    """
    Classe créant la page permettant à un nouveau joueur de créer un nouveau profil.
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.pseudo = self.add_widget(TextInput(self, self.loop, "Pseudo", None))
        self.password = self.add_widget(PasswordInput(self, self.loop, "Password", None))
        self.add_widget(Button(self, self.loop, "Entrer", lambda : LoginPage.test(self, onRegisterPage=True)))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))

class GameMenu(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.add_widget(Button(self, self.loop, "Jouer", lambda: self.next_page(InGameMenu)))
        self.add_widget(Button(self, self.loop, "Controles", lambda: self.next_page(CtrlsPage)))
        self.add_widget(Button(self, self.loop, "Regles", lambda: self.next_page(RulesPage)))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))


class RulesPage(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        rules_text = open(constantes.RULES_TEXT, 'r').read()

        self.add_widget(TextDisplay(self, self.loop, rules_text))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(GameMenu)))


class CtrlsPage(Menu):
    """
    Classe créant la page d'explication des contrôles du jeu
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        controls_text = open(constantes.CTRLS_TEXT, 'r').read()

        self.add_widget(TextDisplay(self, self.loop, controls_text))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(GameMenu)))


class HighscoresPage(Menu):
    """
    Classe créant la page affichant les highscores du jeu ou du joueur s'il est loggé.
    """

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.add_widget(TextDisplay(self, self.loop, "En cours de développement"))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))

    def content(self):
        scores_list = database.Database().getScores()
        toDisplay = 'Rang    Pseudo    Score    Date\n\n'
        rang = 1

        if len(scores_list) == 0:
            toDisplay += "Pas de score, à toi de jouer!"
        else:
            for elt in scores_list:
                toDisplay += str(rang) +'      '+str(elt[1])+"    "+str(elt[2])+"      "+str(elt[3])+'\n'
                rang += 1


        self.add_widget(TextDisplay(self, self.loop, toDisplay))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(MainMenu)))


class InGameMenu(Menu):
    def __init__(self, window, loop, game_data={"score" : 0, "lives": 3, "n_level": 1}):
        Menu.__init__(self, window, loop)

        self.container.set_margin(672, 10)

        self.game_data = game_data

        self.score_widget = self.add_widget(TextDisplay(self, self.loop, "Score : {}".format(self.game_data["score"])))
        self.lives_widget = self.add_widget(TextDisplay(self, self.loop, "Vies restantes : {}".format(self.game_data["lives"])))

        self.background = None

        self.level = process.Level(self, self.game_data["n_level"], window, loop)

    def update_score(self, points):
        self.game_data["score"] += points

        self.score_widget.text = "Score : {}".format(self.game_data["score"])
        self.score_widget.update_text()

    def update_lives(self):
        self.game_data["lives"] -= 1

        if self.game_data["lives"] == 0:
            self.next_page(EndGameMenu, self.game_data)

        else:
            self.lives_widget.text = "Vies restantes : {}".format(self.game_data["lives"])
            self.lives_widget.update_text()

    def keydown(self, event):
        if event.key in constantes.ARROW_KEYS:
            self.level.pacman.change_direction(constantes.ARROW_KEYS[event.key])

        elif event.key == 112:
            if not self.level.pause:
                self.pause()
            else:
                self.resume()

    def tic(self):
        self.level.game_tic()

        self.render()

    def end_level(self):
        self.next_page(NextLevelMenu, self.game_data)

    def pause(self):
        pass

    def resume(self):
        pass



class NextLevelMenu(Menu):
    def __init__(self, window, loop, game_data):
        Menu.__init__(self, window, loop)

        self.game_data = game_data

        self.add_widget(TextDisplay(self, self.loop, "Bravo ! Vous avez réussi le niveau {}".format(self.game_data["n_level"])))
        self.add_widget(Button(self, self.loop, "Continuer", self.next_level))

    def next_level(self):
        self.game_data["n_level"] += 1

        self.next_page(InGameMenu, self.game_data)

class EndGameMenu(Menu):
    def __init__(self, window, loop, game_data):
        Menu.__init__(self, window, loop)

        self.game_data = game_data

        text = """Jeu terminé !
Vous avez obtenu le score de {} points
et atteint le niveau {}""".format(self.game_data["score"], self.game_data["n_level"])

        self.add_widget(TextDisplay(self, self.loop, text))
        self.add_widget(Button(self, self.loop, "Retour", lambda: self.next_page(GameMenu)))
