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

    def add_button(self, text, callback):
        button = Button(self.window, text, callback, self.loop)

        self.l_widgets.append(button)

        return button

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

            widget.render()


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

        self.surface = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()

        # Ajout du bouton dans la boucle pour que celle-ci détecte les clics sur le bouton
        self.loop.add_button(self)

    def render(self):

        # Positionnement du bouton dans la fenêtre
        self.window.blit(self.surface, self.coords)

        # Chargement de la police + taille de la police
        font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.MENUFONT_SIZE)
        self.text_surface = font.render(self.text, 0, constantes.RGB_WHITE)

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