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

    def __init__(self, window, loop, user=""):
        self.loop = loop
        self.window = window
        self.user = user

        self.background = pygame.image.load(constantes.PATH_PIC_PAGES).convert()

        self.container = Container(self, 200, 100)

        self.event_widgets = [] # Liste contenant tous les widgets liés à des évènements

        if self.user:
            self.add_widget(TextDisplay(self, "Connecté en tant que {}\n".format(self.user)))

        self.loop.page = self
        self.focus = None

        # Ajoute un widget pour que le pseudo du joueur apparaisse sur toutes les pages du menu
        # self.pseudo = self.add_widget(TextDisplay(self, "Connecté en tant que {}".format(self.loop.player)))

    def next_page(self, page, *args, **kwargs):
        print("next : " + self.user)
        page(self.window, self.loop, self.user, *args, **kwargs) # Instanciation de la page

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

    def empty(self):
        self.container.empty()
        self.event_widgets = []

    def alert(self, message, action, button_label="Ok"):
        self.empty()

        print("alert : " + self.user)

        self.add_widget(TextDisplay(self, message))
        self.add_widget(Button(self, button_label, action))

class MainMenu(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)
        # Changement du fond
        self.background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
        
        # Marges du haut et du bas pour le conteneur (espace occupé par des éléments du fonds)
        self.container.set_margin(260, 100)

        # Widgets de la page
        self.add_widget(Button(self, "Connexion", lambda: self.next_page(LoginPage)))
        self.add_widget(Button(self, "Inscription", lambda: self.next_page(RegisterPage)))
        self.add_widget(Button(self, "Top Scores", lambda: self.next_page(HighscoresPage)))
        self.add_widget(Button(self, "Quitter", self.loop.close_window))

        # Lancement de la boucle d'évènement si celle-ci n'a pas encore été lancée (ouverture du programme)
        if not self.loop.loop_running:
            self.loop.run_loop()

class LoginPage(Menu):
    """
    Classe créant la page permettant à un joueur existant de se logger.
    """

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.user_input = self.add_widget(TextInput(self, "Pseudo", None))
        self.password = self.add_widget(PasswordInput(self, "Password", None))
        self.add_widget(Button(self, "Entrer", self.submit))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))

    def submit(self):
        user = self.user_input.get()
        password = self.password.get()

        if user and password:

            db = database.Database()

            test = db.testPlayer(user, password)

            if test == 0:
                self.user = user

                message = """Authentification réalisée avec succès !
Vous êtes désormais connecté sous le pseudo {}""".format(user)
                
                print("submit : " + self.user)
                self.alert(message, lambda : self.next_page(GameMenu))

            elif test == 1:
                self.alert("Le mot de passe ne correspond pas\nau nom d'utilisateur !", lambda : self.next_page(LoginPage))

            else:
                self.alert("Ce nom d'utilisateur n'existe pas !", lambda : self.next_page(LoginPage))

        else:
            self.alert("Veuillez remplir tous les champs !", lambda : self.next_page(LoginPage))
            

class RegisterPage(Menu):
    """
    Classe créant la page permettant à un nouveau joueur de créer un nouveau profil.
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.user_input = self.add_widget(TextInput(self, "Pseudo", None))
        self.password = self.add_widget(PasswordInput(self, "Password", None))
        self.confirm = self.add_widget(PasswordInput(self, "Confirmation", None))

        self.add_widget(Button(self, "Entrer", self.submit))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))

    def submit(self):
        user = self.user_input.get()
        password = self.password.get()
        confirm = self.confirm.get()

        if user and password and confirm:
            db = database.Database()

            # Si le nom d'utilisateur existe déjà (code 0 et 1 avec db.testplayer)
            if not db.testPlayer(user) == 2:
                self.alert("Ce nom d'utilisateur est déjà utilisé !", lambda : self.next_page(RegisterPage))

            # Si le mot de passe n'est pas le même deux fois
            elif not password == confirm:
                self.alert("Le mot de passe fourni dans les deux champs\ndoit être identique", lambda : self.next_page(RegisterPage))

            else:
                db.newPlayer(user, password)
                self.user = user

                message = """Enregistrement réalisée avec succès !
Vous êtes désormais connecté sous le pseudo {}""".format(user)
                self.alert(message, lambda : self.next_page(GameMenu))

        else:
            self.alert("Veuillez remplir tous les champs !", lambda : self.next_page(RegisterPage))

class GameMenu(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.add_widget(Button(self, "Jouer", lambda: self.next_page(InGameMenu)))
        self.add_widget(Button(self, "Controles", lambda: self.next_page(CtrlsPage)))
        self.add_widget(Button(self, "Regles", lambda: self.next_page(RulesPage)))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))


class RulesPage(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        rules_text = open(constantes.RULES_TEXT, 'r').read()

        self.add_widget(TextDisplay(self, rules_text))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(GameMenu)))


class CtrlsPage(Menu):
    """
    Classe créant la page d'explication des contrôles du jeu
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        controls_text = open(constantes.CTRLS_TEXT, 'r').read()

        self.add_widget(TextDisplay(self, controls_text))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(GameMenu)))


class HighscoresPage(Menu):
    """
    Classe créant la page affichant les highscores du jeu ou du joueur s'il est loggé.
    """

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        # scores_list = database.Database().getScores()
        # toDisplay = 'Rang    Pseudo    Score    Date\n\n'
        # rang = 1

        # if len(scores_list) == 0:
        #     toDisplay += "Pas de score, à toi de jouer!"
        # else:
        #     for elt in scores_list:
        #         toDisplay += str(rang) +'      '+str(elt[1])+"    "+str(elt[2])+"      "+str(elt[3])+'\n'
        #         rang += 1

        db = database.Database()
        best_scores = db.getScores()


        self.add_widget(Table(self, best_scores))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))


class InGameMenu(Menu):
    def __init__(self, window, loop, user, game_data=None):
        Menu.__init__(self, window, loop, user)

        print("ingame :" + self.user)

        if not game_data:
            self.game_data = {"score" : 0, "lives": 3, "n_level": 1}
        else:
            self.game_data = game_data

        self.container.set_margin(672, 10)

        self.score_widget = self.add_widget(TextDisplay(self, "Score : {}".format(self.game_data["score"])))
        self.lives_widget = self.add_widget(TextDisplay(self, "Vies restantes : {}".format(self.game_data["lives"])))

        self.background = None
        self.pause = False

        self.level = process.Level(self, self.game_data["n_level"], window, loop)

    def update_score(self, points):
        self.game_data["score"] += points

        self.score_widget.text = "Score : {}".format(self.game_data["score"])
        self.score_widget.update_text()

    def update_lives(self):
        self.game_data["lives"] -= 1

        if self.game_data["lives"] == 0:
            self.end_game()

        else:
            self.lives_widget.text = "Vies restantes : {}".format(self.game_data["lives"])
            self.lives_widget.update_text()

    def end_game(self):
        self.pause_game()
        db = database.Database()
        # Enregistrement du score dans la base de données
        db.newScore(self.user, self.game_data["score"])
        db.close() # Fermeture de la connexion à la db

        # Affichage du message de fin de partie
        message = """Jeu terminé !
Vous avez obtenu le score de {} points
et atteint le niveau {}""".format(self.game_data["score"], self.game_data["n_level"])
        
        self.alert(message, lambda : self.next_page(MainMenu), "Menu principal")

    def keydown(self, event):
        if not self.pause:
            if event.key in constantes.ARROW_KEYS:
                self.level.pacman.change_direction(constantes.ARROW_KEYS[event.key])

            elif event.key == 112:
                if not self.pause:
                    self.pause_game()

                    self.add_widget(Button(self, "Reprendre", self.resume))
                    self.add_widget(Button(self, "Menu principal", self.leave_game))
                    self.add_widget(self.score_widget)
                    self.add_widget(self.lives_widget)

                else:
                    self.resume()

    def tic(self):
        self.level.game_tic()

        self.render()

    def end_level(self):
        message = "Bravo ! Vous avez réussi le niveau {}".format(self.game_data["n_level"])

        self.pause_game()
        self.alert(message, lambda : self.next_page(InGameMenu))

        self.game_data["n_level"] += 1

    def pause_game(self):
        self.empty()
        self.pause = True
        self.background = pygame.image.load(constantes.PATH_PIC_PAGES).convert()

        self.container.set_margin(200, 100)

    def resume(self):
        self.empty()
        self.background = None
        self.container.set_margin(672, 10)

        self.add_widget(self.score_widget)
        self.add_widget(self.lives_widget)

        self.pause = False

    def leave_game(self):
        self.empty()
        self.add_widget(TextDisplay(self, "Voulez-vous vraiment retourner\nau menu principal ?"))
        self.add_widget(Button(self, "Oui", lambda : self.next_page(MainMenu)))
        self.add_widget(Button(self, "Annuler", self.pause))
