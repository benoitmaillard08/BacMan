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
		self.loop_running = False

		self.page = None

	def run_loop(self):
		"""
		run_loop() --> None
		Lance la boucle
		"""
		self.loop_running = True

		# Tant que l'utilisateur n'appuie pas sur la croix de fermeture
		while self.window_opened:
			t1 = time.clock() # Lancement du chrono de l'itération
			
			if self.page: # Si une page de menu est ouverte
				self.page.tic()

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

			pygame.display.flip() # Rafraichissement du rendu

		pygame.display.quit()


	def close_window(self):
		"""
		close_window() --> None
		Indique que la fenêtre doit être fermée
		"""
		self.window_opened = False
