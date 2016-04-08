import pygame
import constantes
from pygame.locals import *

class Container:
    MARGIN = 10
    """
    Conteneur de widgets pour que ceux-ci soient centrés horizontalement et verticalement
    """

    def __init__(self, page, margin_top=0, margin_bottom=0):
        self.page = page

        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

        # Liste des widgets du container
        self.l_widgets = []

    def add_widget(self, widget):
        """
        add_widget(Widget widget) --> Widget
        Ajoute un widget au container
        """
        self.l_widgets.append(widget)

        # Place le widget
        self.calculate_coords()

        return widget

    def set_margin(self, top, bottom):
        """
        set_margin(int top, int bottom) --> None
        Permet de définir une marge en haut et en bas de la fenêtre qui ne
        doit pas être occupée par des widgets
        """
        self.margin_top = top
        self.margin_bottom = bottom

    def calculate_coords(self):
        """
        calculate_coords() --> None
        Calcul des coordonnées des widgets
        """
        # Hauteur de la pile d'éléments
        total_height = 0

        for widget in self.l_widgets:
            total_height += widget.get_height() + 2 * Container.MARGIN

        # Coordonné y du coin supérieur gauche du premier widget
        coord_y = (self.page.window.get_height() - self.margin_top - self.margin_bottom - total_height) / 2 + self.margin_top

        for widget in self.l_widgets:
            # Coordonné x du coin supérieur gauche du widget
            coord_x = (self.page.window.get_width() - widget.get_width()) / 2
            widget.set_coords(coord_x, coord_y + Container.MARGIN) # Définition des coordonnées du widget

            # La coordonnée y est augmentée pour le widget suivant
            coord_y += widget.get_height() + 2 * Container.MARGIN

    def render(self):
        """
        render() --> None
        Rendu de tous les widgets du container
        """
        for widget in self.l_widgets:
            widget.render()

    def empty(self):
        """
        empty() --> None
        Supprime tous les widgets du container
        """
        self.l_widgets = []


class Button:
    """
    Bouton avec du texte et une action à réaliser lors du cliq
    """
    def __init__(self, page, label, callback, directory=constantes.PATH_PIC_BUTTON):
        """
        __init__() --> None.
        """

        self.coords = (0, 0)

        self.label = label
        self.page = page    # variable 'background' de la classe 'MainMenu'
        self.action = callback # fonction à exécuter lors du clic sur le bouton
        self.event = True

        # Chargement de la texture du bouton
        self.surface = pygame.image.load(directory).convert_alpha()

        # Chargement de la police + taille de la police
        self.font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.TEXTFONT_SIZE)
        self.label_surface = self.font.render(self.label, 0, constantes.RGB_WHITE)

        self.text_surface = self.label_surface

    def render(self):
        """
        render() --> None
        Rendu du widget
        """

        # Positionnement du bouton dans la fenêtre
        self.page.window.blit(self.surface, self.coords)

        # Raccourcis
        b = self.surface
        t = self.text_surface

        #Affichage du texte en fonction de sa taille et celle du bouton, afin qu'il soit centré quelque soit sa taille
        self.page.window.blit(self.text_surface, (
            (self.coords[0] + b.get_width() / 2) - t.get_width() / 2,
            (self.coords[1] + b.get_height() / 2) - t.get_height() / 2
        ))

    def get_height(self):
        """
        get_height() --> int
        Retourne la hauteur du widget
        """
        return self.surface.get_height()

    def get_width(self):
        """
        get_width() --> int
        Retourne la largeur du widget
        """
        return self.surface.get_width()

    def set_coords(self, x, y):
        """
        set_coords(int x, int y) --> None
        Définit les coordonnées du widget
        """
        self.coords = (x, y)

    def check_coords(self, coords):
        """
        check_coords(tuple coords) --> bool
        Renvoie True si les coordonnées en argument sont à l'intérieur la surface du widget
        """
        if self.coords[0] < coords[0] < self.coords[0] + self.surface.get_width():
            if self.coords[1] < coords[1] < self.coords[1] + self.surface.get_height():
                return True

        else:
            return False

class TextInput(Button):
    """
    Champ de formulaire
    """
    def __init__(self, page, label, callback, max_length=15):
        Button.__init__(self, page, label, callback)

        # Lors d'un cliq sur le champ, ce dernier obtient le focus
        self.action = self.set_focus
        self.content = ""
        self.max_length = max_length

        self.content_surface = self.font.render(self.content, 0, constantes.RGB_WHITE)

    def set_focus(self):
        """
        set_focus() --> None
        Place le focus sur le widget
        """

        self.page.focus_on(self)

        self.text_surface = self.content_surface

    def remove_focus(self):
        """
        remove_focus() --> None
        Retire le focus du widget
        """
        # Si aucun texte n'a été rentré, on réaffiche le label
        if len(self.content) == 0:
            self.text_surface = self.label_surface

    def keydown(self, event):
        """
        keydown(pygame.event event) --> None
        Signale un évènement au widget
        """
        # Touches alphanumériques
        if chr(event.key) in constantes.KEYS and len(self.content) < self.max_length:
            self.content = self.content + chr(event.key)

        # Touche pour effacer
        elif event.key == 8:
            if self.content:
                self.content = self.content[:-1]

        self.update_text()


    def update_text(self):
        """
        update_text() --> None
        Met à jour le contenu du champ
        """
        # Mise à jour de la surface pygame pour le texte
        self.content_surface = self.font.render(self.content, 0, constantes.RGB_WHITE)

        self.text_surface = self.content_surface

    def get(self):
        """
        get() --> str
        Retourne le contenu du champ
        """
        return self.content

class PasswordInput(TextInput):
    """
    Champ de formulaire avec contenu caché (pour les mots de passe)
    """
    def update_text(self):
        """
        update_text() --> None
        Met à jour le contenu du champ en affichant des "*"
        """

        # Chaîne de la longueur du contenu du champ avec des *
        self.string = "*" * len(self.content)

        # Mise à jour de la surface avec les ***
        self.content_surface = self.font.render(self.string, 0, constantes.RGB_WHITE)

        self.text_surface = self.content_surface


class TextDisplay:
    """
    Zone d'affichage de texte
    """

    def __init__(self, page, text):
        self.coords = (0, 0)

        self.page = page
        self.text = text

        self.event = False

        # Chargement de la police + taille de la police
        self.font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)

        self.update_text()

    def render(self):
        """
        render() --> None
        Rendu du widget
        """

        line_y = self.coords[1]

        for line in self.lines_surfaces:
            line_x = self.coords[0] + (self.get_width() - line.get_width()) / 2

            self.page.window.blit(line, (line_x, line_y))

            line_y += line.get_height()


    def get_height(self):
        """
        get_height() --> int
        Retourne la hauteur du widget
        """

        height = 0

        for surface in self.lines_surfaces:
            height += surface.get_height()

        return height

    def get_width(self):
        """
        get_width() --> None
        Retourne la largeur du widget
        """
        max_width = 0

        # La largeur du widget correspond à la largeur de la ligne la plus longue
        for surface in self.lines_surfaces:
            if surface.get_width() > max_width:
                max_width = surface.get_width()

        return max_width

    def set_coords(self, x, y):
        """
        set_coords(int x, int y) --> None
        Définit les coordonnées du widget
        """
        self.coords = (x, y)

    def check_coords(self, event):
        """
        check_coords(pygame.event event) --> bool
        Retourne False à chaque fois car ce widget n'est pas
        concerné par les évènements
        """
        return False

    def update_text(self):
        """
        update_text() --> None
        Créé les surfaces pygame pour l'affichage du texte
        """
        self.lines_surfaces = []

        # Construction des surfaces pygame pour chaque ligne
        for line in self.text.split("\n"):
            line_surface = self.font.render(line, 0, constantes.RGB_WHITE)
            self.lines_surfaces.append(line_surface)

class Table(TextDisplay):
    """
    Widget permettant d'afficher des données (liste de listes) sous forme de tableau
    """
    def __init__(self, page, data):
        TextDisplay.__init__(self, page, "")

        # Données du tableau inversées --> Les colonnes deviennent les lignes et vice versa
        inverted_data = list(zip(*data))

        # Liste des strings pour chaque ligne
        data_str = [""] * len(data)

        for col in inverted_data:

            # Nombre de caractères nécessaires pour la colonne
            col_length = len(str(max(col, key=lambda n: len(str(n))))) + 5

            for i in range(len(col)):
                # Ajout des espaces nécessaires
                spaces_to_add = " " * (col_length - len(str(col[i])))
                data_str[i] += (str(col[i]) + spaces_to_add)

        # Toutes les lignes sont appondues avec un retour à la ligne entre chacune
        for i in range(len(data_str)):
            data_str[i] = data_str[i][:-5] # On supprime les espaces inutiles à la fin de chaque ligne

        self.text = "\n".join(data_str) # Les lignes sont appondues avec un retour à la ligne entre chaque

        self.update_text()
