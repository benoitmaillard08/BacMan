import time
import pygame
from constantes import *

class Loop:
	"""
	Boucle permettant de gérer les évènements, les mouvements du jeu ainsi que
	le rafraichissement de l'image
	"""
	def __init__(self, level=None):
		self.window_opened = True
		self.level = level
		self.loop_running = False

		self.widgets = []

		self.focus = None
		self.page = None

	def run_loop(self):
		"""
		Lance la boucle
		"""
		self.loop_running = True

		# Tant que l'utilisateur n'appuie pas sur la croix de fermeture
		while self.window_opened:
			t1 = time.clock() # Lancement du chrono de l'itération

			if self.level: # Si un niveau est lancé
				self.level.game_tic()
			
			if self.page: # Si une page de menu est ouverte
				self.page.render()

			# Gestion des évènements
			for event in pygame.event.get():

				# Fermeture
				if event.type == pygame.QUIT:
					self.window_opened = False

				else:
					self.page.event(event)

			t2 = time.clock() # Fin du chrono de l'itération

			tic_duration = t2 - t1 # Temps restant avant le rafraichissement optimal de la fenêtre
			time_remaining = 0.06 - tic_duration


			# Si l'itération a duré moins longtemps que la durée optimale prévue,
			# il faut encore attendre pour que le jeu soit fluide
			if time_remaining > 0:
				time.sleep(time_remaining)
			else:
				print(time_remaining)

			pygame.display.flip() # Rafraichissement du rendu

		pygame.display.quit()

	def clear(self):
		"""
		Permet de supprimer tout le contenu d'une page de menu
		"""
		self.widgets = []
		self.focus = None

	def clear_level(self):
		self.level = None

	def focus_on(self, widget):
		"""
		Donne le focus à un widget
		"""
		self.focus = widget

	def close_window(self):
		"""
		Indique que la fenêtre doit être fermée
		"""
		self.window_opened = False

	def add_widget(self, widget):
		"""
		Permet d'ajouter un widget à la liste des widgets pris en compte par la boucle
		"""
		self.widgets.append(widget)
