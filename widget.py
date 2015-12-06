import pygame
import constantes
from pygame.locals import *

class InputBox:
	"""
	Classe instanciant la zone d'entrée permettant au joueur de par exemple s'enregistrer.
	"""
	def __init__(self, window):
		pygame.init()

		self.window = window


	def compiler(self, liste):
		"""
		compiler(list liste) --> str
		Méthode permettant de transformer la liste de caractères entrée en chaîne de caractères.
		"""
		string = ''

		for elt in liste:
			string += elt

		return

	def entry(self):
		"""
		inputBox() --> str pseudo
		Méthode recevant les entrées de l'utilisateur.
		"""
		entry_list = []
		ready = False

		while not ready:
			for event in pygame.event.get():
				if event.type == KEYDOWN and len(entry_list)<16:
					if chr(event.key) in constantes.KEYS:
						entry += chr(event.key)

					elif event.key == 8: 	 # 8 --> code du backspace (pour effacer)
						if entry_list: 		# On vérifie si la liste n'est pas vide
							del entry[-1]

					elif event.key == 13:	 # 13 --> code du retour à la ligne (Enter)
						self.pseudo = compiler(entry_list)
						ready = True

					else:
						# Indique à l'utilisateur que le caractère entré n'est pas autorisé.
						pass

	def display(self):
		"""
		Méthode permettant d'afficher la zone d'entré dans la fenêtre <window>.
		"""

class Container:
    MARGIN = 10
    """
    Classe créant un conteneur de boutons pour que ceux-ci soient centrés horizontalement et verticalement
    """

    def __init__(self, window, loop, margin_top=0, margin_bottom=0):
        self.window = window
        self.loop = loop

        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

        self.l_widgets = []

    def add_widget(self, widget):
        self.l_widgets.append(widget)

        return widget

    def set_margin(self, top, bottom):
        self.margin_top = top
        self.margin_bottom = bottom

    def calculate_coords(self):
        # Hauteur de la pile d'éléments

        total_height = 0
        for widget in self.l_widgets:
            total_height += widget.surface.get_height() + 2 * Container.MARGIN

        # Coordonné y du coin supérieur gauche du premier widget
        coord_y = (self.window.get_height() - self.margin_top - self.margin_bottom - total_height) / 2 + self.margin_top

        for widget in self.l_widgets:
            # Coordonné x du coin supérieur gauche du widget
            coord_x = (self.window.get_width() - widget.surface.get_width()) / 2
            widget.set_coords(coord_x, coord_y + Container.MARGIN)
            coord_y += widget.surface.get_height() + 2 * Container.MARGIN

    def render(self):
        for widget in self.l_widgets:
            widget.render()


class Button:
    """
    Classe d'instenciation des boutons
    """
    def __init__(self, window, loop, label, callback):
        """
        __init__() --> None.
        """

        self.coords = (0, 0)

        self.label = label
        self.window = window    # variable 'background' de la classe 'MainMenu'
        self.action = callback # fonction à exécuter lors du clic sur le bouton
        self.loop = loop

        # Chargement de la texture du bouton
        self.surface = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()

        # Chargement de la police + taille de la police
        self.font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.TEXTFONT_SIZE)
        self.label_surface = self.font.render(self.label, 0, constantes.RGB_WHITE)

        self.text_surface = self.label_surface

        # Ajout du bouton dans la boucle pour que celle-ci détecte les clics sur le bouton
        self.loop.add_widget(self)

    def render(self):

        # Positionnement du bouton dans la fenêtre
        self.window.blit(self.surface, self.coords)

        # Raccourcis
        b = self.surface
        t = self.text_surface

        #Affichage du texte en fonction de sa taille et celle du bouton, afin qu'il soit centré quelque soit sa taille
        self.window.blit(self.text_surface, (
            (self.coords[0] + b.get_width() / 2) - t.get_width() / 2,
            (self.coords[1] + b.get_height() / 2) - t.get_height() / 2
        ))

    def set_coords(self, x, y):
        self.coords = (x, y)

    def check_coords(self, coords):
        if self.coords[0] < coords[0] < self.coords[0] + self.surface.get_width():
            if self.coords[1] < coords[1] < self.coords[1] + self.surface.get_height():
                return True

        return False

    def disable(self):
        pass

    def enable(self):
        pass

class TextInput(Button):
    def __init__(self, window, loop, label, callback, max_length=20):
        Button.__init__(self, window, loop, label, callback)

        # Lors d'un cliq sur le champ, ce dernier obtient le focus
        self.action = self.set_focus
        self.content = ""
        self.max_length = max_length

        self.content_surface = self.font.render(self.content, 0, constantes.RGB_WHITE)

    def set_focus(self):
        self.loop.focus_on(self)

        self.focus = True

        self.text_surface = self.content_surface

    def remove_focus(self):
        self.focus = False

        if len(self.content) == 0:
            self.text_surface = self.label_surface

    def keydown(self, event):
        if chr(event.key) in constantes.KEYS and len(self.content) < self.max_length:
            self.content = self.content + chr(event.key)

        elif event.key == 8:
            if self.content:
                self.content = self.content[:-1]

        elif event.key == 13:
            
            pass ### Donne le focus au widget suivant

        self.content_surface = self.font.render(self.content, 0, constantes.RGB_WHITE)

        self.text_surface = self.content_surface


class TextDisplay:
    """
    Widget permettant d'afficher du texte sur plusieurs lignes et de manière centrée.
    """
    def __init__(self, window, text, line=300):
        """
        __init__(window, str text, int line) --> None. On entre le chemin du fichier texte à lire pour la var 'text'.
        """

        self.window = window
        self.line = line

        # Chargement du texte à afficher dans une liste, ligne par ligne.
        self.text_to_display = open(text, 'r').read().split('\n')

        # Chargement de la police
        self.font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)


    def display(self):

        for elt in self.text_to_display: # Pour chaque ligne de texte, on crée un nouvel objet text.

            size = self.font.size(elt)[0] # Pour centrer le texte
            text_line = self.font.render(elt, 0, constantes.RGB_WHITE)
            
            self.window.blit(text_line, ((self.window.get_width()//2 - size//2), self.line)) # 'Collage' de la ligne, avec 25 pixels de marge à gauche
            self.line += constantes.TEXTFONT_SIZE + 10  #La position de la prochaine ligne est placée à 25 + 10 pixels plus bas