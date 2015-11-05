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
		fenetre = pygame.display.set_mode((constantes.COTE_FOND, constantes.COTE_FOND), RESIZABLE)

		# Importation des images
		# Menu
		background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
		fenetre.blit(background,(0,0))

		###########
		# Boutons #
		###########

		# Controles

		button_ctrl = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()
		# Positionnement du bouton dans la fenêtre
		fenetre.blit(button_ctrl, constantes.POS_CTRL_BUT)

		#---------------

		# Rafrachissement de l'écran
		pygame.display.flip()


		flag = 1

		while flag:
			for event in pygame.event.get(): 	# Parcours la liste des éléments reçus
				if event.type == QUIT:
					flag = 0
				elif event.type == MOUSEBUTTONDOWN and event.button == 1:
					x = event.pos[1] 	#Les positions du clic de la souris sont enregistrés pour être analyser
					y = event.pos[0]




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

		

				



