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
    Classe abstraite définissant une page de menu du jeu
    """

    def __init__(self, window, loop, user=""):
        self.loop = loop
        self.window = window
        self.user = user # Chaine contenant le pseudo du joueur (si l'utilisateur est connecté)

        self.background = pygame.image.load(constantes.PATH_PIC_PAGES).convert()

        # Container qui s'occupera de placer les widgets de la page de manière correcte
        self.container = Container(self, 200, 100)

        self.event_widgets = [] # Liste contenant tous les widgets liés à des évènements

        # Affichage du pseudo du joueur
        if self.user:
            self.add_widget(TextDisplay(self, "Connecté en tant que {}\n".format(self.user)))

        self.loop.page = self
        self.focus = None

        # Ajoute un widget pour que le pseudo du joueur apparaisse sur toutes les pages du menu
        # self.pseudo = self.add_widget(TextDisplay(self, "Connecté en tant que {}".format(self.loop.player)))

    def next_page(self, page, *args, **kwargs):
        """
        next_page(Menu page, *args, **kwargs) --> None
        Raccourci pour ouvrir une nouvelle page de menu
        """
        
        page(self.window, self.loop, self.user, *args, **kwargs) # Instanciation de la page

    def tic(self):
        """
        tic() --> None
        Action réalisée sur la page à itération de la boucle.
        """
        self.render()

    def render(self):
        """
        render() --> None
        Affiche le rendu de la page
        """
        if self.background:
            self.window.blit(self.background,(0,0)) # Rendu du fonds

        # Rendu des widgets
        self.container.render()

    def add_widget(self, widget):
        """
        add_widget(Widget widget) --> Widget
        Permet d'ajouter un widget sur la page
        """
        # si un event est lié au widget
        if widget.event:
            self.event_widgets.append(widget)

        # Tous les widgets sont ajoutés au container 
        self.container.add_widget(widget)

        return widget

    def event(self, event):
        """
        event(pygame.event event) --> None
        Permet de transmettre à la page de menu un évènement
        """
        # Si l'évènement est un cliq
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if self.focus: # Si un widget a le focus, le focus lui est retiré
                    self.focus.remove_focus()
                    self.focus = None

                # On regarde si le cliq concerne un widget
                for widget in self.event_widgets:
                    if widget.check_coords(event.pos): # On regarde si l'utilisateur a cliqué sur un widget
                        widget.action()
                        break

        # S'il s'agit d'une touche du clavier
        elif event.type == pygame.KEYDOWN:
            # Si un widget a le focus sur la page
            if self.focus:
                self.focus.keydown(event)

            else:
                self.keydown(event)

    def keydown(self, event):
        """
        keydown(pygame.event event) --> None
        Permet de transmettre la pression d'une touche du clavier à la page
        Méthode destinée à être surchargée
        """
        pass

    def focus_on(self, widget):
        """
        focus_on(Widget widget) --> None
        Donne le focus au widget
        """
        self.focus = widget

    def empty(self):
        """
        empty() --> None
        Supprime tous les widgets du container et de la liste
        des widgets liés à des évènements
        """
        self.container.empty()
        self.event_widgets = []

    def alert(self, message, action, button_label="Ok"):
        """
        alert(str message, function action, str button_label) --> None
        Raccourci permettant d'afficher un message d'alerte avec un bouton.
        L'action à réaliser lorsque l'utilisateur clique sur le bouton peut être
        définie avec le paramètre action
        """
        # Les widgets sont supprimés
        self.empty()

        self.add_widget(TextDisplay(self, message)) # Affichage du message
        self.add_widget(Button(self, button_label, action))

class MainMenu(Menu):
    """
    Menu principal du jeu
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)
        # Changement du fond
        self.background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
        
        # Marges du haut et du bas pour le conteneur (espace occupé par des éléments du fonds)
        self.container.set_margin(260, 100)

        # Widgets de la page
        if self.user:
            self.add_widget(Button(self, "Menu de jeu", lambda : self.next_page(GameMenu)))
        else:
            self.add_widget(Button(self, "Connexion", lambda: self.next_page(LoginPage)))
            self.add_widget(Button(self, "Inscription", lambda: self.next_page(RegisterPage)))

        self.add_widget(Button(self, "Top Scores", lambda: self.next_page(HighscoresPage)))
        self.add_widget(Button(self, "Quitter", self.loop.close_window))

        # Lancement de la boucle d'évènement si celle-ci n'a pas encore été lancée (ouverture du programme)
        if not self.loop.loop_running:
            self.loop.run_loop()

class LoginPage(Menu):
    """
    Page permettant à un joueur de se logger
    """

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.user_input = self.add_widget(TextInput(self, "Pseudo", None))
        self.password = self.add_widget(PasswordInput(self, "Password", None))
        self.add_widget(Button(self, "Entrer", self.submit))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))

    def submit(self):
        """
        submit() --> None
        Soumets les données entrées dans le formulaire et vérifie celles-ci.
        Renvoie un message d'erreur en conséquence si besoin
        """
        # Récupération des données
        user = self.user_input.get()
        password = self.password.get()

        # Si les champs ont été complétés
        if user and password:
            # Connexion à la base de données
            db = database.Database()

            test = db.testPlayer(user, password)

            db.close()

            # Si les données sont correctes
            if test == 0:
                self.user = user

                message = """Authentification réalisée avec succès !
Bon retour parmis nous, {}!""".format(user)
                
                
                self.alert(message, lambda : self.next_page(GameMenu))

            # Si le pseudo et le mdp ne correspondent pas
            elif test == 1:
                self.alert("Le mot de passe ne correspond pas\nau nom d'utilisateur !", lambda : self.next_page(LoginPage))

            # Si le pseudo n'existe pas
            else:
                self.alert("Ce nom d'utilisateur n'existe pas !", lambda : self.next_page(LoginPage))

        else:
            self.alert("Veuillez remplir tous les champs !", lambda : self.next_page(LoginPage))
            

class RegisterPage(Menu):
    """
    Page permettant à un nouveau joueur de s'enregistrer
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.surname = self.add_widget(TextInput(self, "Nom", None))
        self.name = self.add_widget(TextInput(self, "Prenom", None))
        self.user_input = self.add_widget(TextInput(self, "Pseudo", None))
        self.password = self.add_widget(PasswordInput(self, "Password", None))
        self.confirm = self.add_widget(PasswordInput(self, "Confirmation", None))

        self.add_widget(Button(self, "Entrer", self.submit))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))

    def submit(self):
        """
        submit() --> None
        Soumets les données entrées dans le formulaire et créé
        un nouvel utilisateur dans la base de données si cela est possible
        Renvoie un message d'erreur en conséquence si besoin
        """
        user = self.user_input.get()
        password = self.password.get()
        name = self.name.get()
        surname = self.surname.get()
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
                db.newPlayer(user, password, surname, name)
                self.user = user

                message = """Enregistrement réalisée avec succès !
Vous êtes désormais connecté sous le pseudo {}""".format(user)
                self.alert(message, lambda : self.next_page(GameMenu))

            db.close()

        else:
            self.alert("Veuillez remplir tous les champs !", lambda : self.next_page(RegisterPage))

class GameMenu(Menu):
    """
    Menu permettant l'accès au jeu et aux indications de jeu
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.add_widget(Button(self, "Jouer", lambda: self.next_page(InGameMenu)))
        self.add_widget(Button(self, "Niveaux", lambda: self.next_page(LevelSelector)))
        self.add_widget(Button(self, "Controles", lambda: self.next_page(CtrlsPage)))
        self.add_widget(Button(self, "Regles", lambda: self.next_page(RulesPage)))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))

# class LevelSelector(Menu):
#     """
#     Page permettant au joueur de commencer une partie au niveau souhaité.
#     """
#     def __init__(self, *args, **kwargs):
#         Menu.__init__(self, *args, **kwargs)

#         # Création des zones de texte/boutons
#         self.add_widget(TextDisplay(self, "Choisissez votre niveau."))
#         try:
#             bestLevel = database.Database().getScores(self.user)[0][2]  # On recherche le meilleur score du joueur.
#         except:
#             bestLevel = 0 # S'il n'a pas encore joué, il peut seulement accéder au niveau 1.

#         for elt in range(bestLevel):
#             self.add_widget(Button(self, str(elt+1), lambda: self.next_page(InGameMenu, self.gameDataInit(elt))))
        

#         self.add_widget(Button(self, "Retour", lambda: self.next_page(GameMenu)))

#     def gameDataInit(self, elt):
#         self.game_data = {"score" : 0, "lives": 3, "n_level": elt+1}
#         return self.game_data



class RulesPage(Menu):
    """
    Page d'explication des règles du jeu
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        # Récupération du texte dans un fichier externe
        rules_text = open(constantes.RULES_TEXT, 'r').read()

        self.add_widget(TextDisplay(self, rules_text))

        self.add_widget(Button(self, "Retour", lambda: self.next_page(GameMenu)))


class CtrlsPage(Menu):
    """
    Page d'explication des contrôles du jeu
    """
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        # Récupération du texte dans un fichier externe
        controls_text = open(constantes.CTRLS_TEXT, 'r').read()

        self.add_widget(TextDisplay(self, controls_text))
        self.add_widget(Button(self, "Retour", lambda: self.next_page(GameMenu)))


class HighscoresPage(Menu):
    """
    Page affichant les highscores du jeu ou du joueur s'il est loggé.
    """

    def __init__(self, window, loop, user, global_scores=False):
        Menu.__init__(self, window, loop, user)

        # Connexion à la db
        db = database.Database()

        # Pour afficher les du joueur, celui-ci doit être connecté
        if self.user and not global_scores:
            best_scores = db.getScores(self.user)


            self.add_widget(Button(self, "Scores globaux", lambda : self.next_page(HighscoresPage, True)))
        else:
            best_scores = db.getScores()

            if self.user:
                self.add_widget(Button(self, "Scores perso", lambda : self.next_page(HighscoresPage)))

        db.close()

        # Conversion en liste de listes pour plus de flexibilité
        best_scores = [list(t) for t in best_scores]

        # Ajout du rang (1, 2, 3, 4, 5)
        for i in range(len(best_scores)):
            best_scores[i].insert(0, i + 1)

        # Ajout du titre des colonnes
        best_scores[0:0] = [["Rang", "Pseudo", "Score", "Niveau atteint", "Date"], [""] * 5]

        # Création d'un tableau
        self.add_widget(Table(self, best_scores))

        self.add_widget(Button(self, "Retour", lambda: self.next_page(MainMenu)))


class InGameMenu(Menu):
    """
    Page gérant le déroulement d'un niveau de jeu
    """
    def __init__(self, window, loop, user, game_data=None):
        Menu.__init__(self, window, loop, user)

        # S'il s'agit du premier niveau, il faut initialiser
        # les données de la partie
        if not game_data:
            self.game_data = {"score" : 0, "lives": 3, "n_level": 1}
        else:
            self.game_data = game_data

        # Adaptation de la marge du container
        self.container.set_margin(672, 10)

        self.end = False # Vaut True si le niveau est terminé

        self.update_table() # Création du tableau avec les données de jeu

        self.background = None # Pas d'image de fond
        self.pause = False # Vaut True si le jeu est en pause

        # Instanciation du niveau
        self.level = process.Level(self, self.game_data["n_level"], window, loop)

        # Lancement de la musique
        try:
            self.music = pygame.mixer.Sound(constantes.SOUND_DIR + 'level{}.wav'.format(self.game_data["n_level"]))
        except: # S'il n'a a pas de musique pour le niveau, on prend celle du lvl 1 (pour le plus grand plaisir du joueur :D )
            self.music = pygame.mixer.Sound(constantes.SOUND_DIR + 'level1.wav')

        self.volume = 1.0
        self.music.play(loops=10000) # la musique doit être jouée en boucle


    def update_table(self):
        """
        update_table() --> None
        Permet de créer/mettre à jour le tableau des données de la partie
        """
        data = [
            ["Pseudo", "Niveau", "Score", "Vies restantes"],
            [self.user, self.game_data["n_level"], self.game_data["score"], self.game_data["lives"]]
        ]

        # On efface le tableau avant de le recréer
        self.empty()

        # Création du widget tableau
        self.add_widget(Table(self, data))

    def update_score(self, points):
        """
        update_score(int points) --> None
        Permet d'ajouter un certain nombre de points
        """
        # ancien score
        old_score = self.game_data["score"]
        self.game_data["score"] += points

        # Tous les 10'000 points, une vie est rajoutée
        if self.game_data["score"] > (old_score//10000+1)*10000:
            self.update_lives(1)
            self.music = pygame.mixer.Sound(constantes.SOUND_DIR + 'extralife.wav')
            self.music.play()

        # Le tableau est mis à jour
        self.update_table()

    def update_lives(self, update=-1):
        """
        update_lives(int update) --> None
        Permet de mettre à jour le nombre de vies. Par défaut,
        enlève une vie.
        """
        self.game_data["lives"] += update

        if self.game_data["lives"] == 0:
            self.end_game()

        else:
            # Le tableau est mis à jour
            self.update_table()

    def end_game(self):
        """
        end_game() --> None
        Permet de mettre fin à la partie. Les données
        de la partie sont enregistrées dans la base de données
        """
        self.end = True
        self.music.stop()

        self.background = pygame.image.load(constantes.PATH_PIC_PAGES).convert()
        self.container.set_margin(200, 100)

        db = database.Database()
        # Enregistrement du score et du niveau dans la base de données
        db.newScore(self.user, self.game_data["score"], self.game_data["n_level"])
        db.close() # Fermeture de la connexion à la db

        # Affichage du message de fin de partie
        message = """Jeu terminé !
Vous avez obtenu le score de {} points
et atteint le niveau {}""".format(self.game_data["score"], self.game_data["n_level"])
        
        self.alert(message, lambda : self.next_page(MainMenu), "Menu principal")

    def keydown(self, event):
        """
        keydown(pygame.event event) --> None
        Gère les pression des touches de clavier
        Touche directionnelles --> direction pacman
        Touche P : pause
        Touche M : musique
        """
        # Il faut vérifier que le niveau n'est pas terminé
        if not self.end:
            if event.key in constantes.ARROW_KEYS:
                self.level.pacman.change_direction(constantes.ARROW_KEYS[event.key])

            elif event.key == 112: # Mise en pause/reprise du jeu
                if not self.pause:
                    self.pause_game()

                else:
                    self.resume()

        # À l'activation de la touche 'M', le volume de la musique uniquement se règle à 0 ou 1.
        if event.key == 109:
            self.volume += 1
            self.music.set_volume(self.volume%2) # À l'activation de la touche 'M', le volume de la musique uniquement se règle à 0 ou 1.

    def tic(self):
        """
        tic() --> None
        Action à effectuer à chaque itération de la boucle
        """
        if not self.end: # Itération du jeu si le niveau n'est pas terminé
            self.level.game_tic()

            # Mise à jour du rendu
            self.render()

    def end_level(self):
        """
        end_level() --> None
        Met fin au niveau et affiche un message pour passer au niveau suivant
        """
        self.music.stop()

        message = "Bravo ! Vous avez réussi le niveau {}".format(self.game_data["n_level"])

        self.end = True # le niveau est terminé

        # Changement du fond
        self.background = self.background = pygame.image.load(constantes.PATH_PIC_PAGES).convert()
        self.container.set_margin(200, 100)

        self.game_data["n_level"] += 1
        self.game_data["score"] += 500 # 500 points bonus à la fin de chaque niveau
        self.alert(message, lambda : self.next_page(InGameMenu, self.game_data))

    def pause_game(self):
        """
        pause_game() --> None
        Permet de mettre en pause le jeu
        """
        self.empty()
        self.pause = True

        # Fond du menu de pause
        self.background = pygame.image.load(constantes.PAUSE_BACKGROUND).convert_alpha()
        self.container.set_margin(260, 100)

        self.add_widget(Button(self, "Reprendre", self.resume))
        self.add_widget(Button(self, "Menu principal", self.leave_game))

    def resume(self):
        """
        resume() --> None
        Permet de reprendre la partie après une pause
        """
        self.empty()
        self.background = None
        self.container.set_margin(672, 10)

        self.update_table()

        self.pause = False

    def leave_game(self):
        """
        leave_game() --> None
        Affiche un message de confirmation pour quitter la partie en cours
        """
        self.empty()
        self.add_widget(TextDisplay(self, "Voulez-vous vraiment retourner\nau menu principal ?"))
        self.add_widget(Button(self, "Oui", lambda : self.rage_quit()))
        self.add_widget(Button(self, "Annuler", self.pause_game))

    def rage_quit(self):
        """
        rage_quit() --> None
        Quitte définitivement la partie en cours
        """
        self.music.stop()
        self.next_page(MainMenu)