import time
import pygame
from constantes import *

class Loop:
	def __init__(self, level=None):
		self.window_opened = True
		self.game_running = False
		self.level = level
		self.loop_running = False

		self.widgets = []

		self.focus = None
		self.page = None

	def run_loop(self):
		self.loop_running = True

		while self.window_opened:
			t1 = time.clock()

			if self.level:
				self.level.game_tic()

			if self.page:
				self.page.render()

			# Check pour la fermeture
			for event in pygame.event.get():
				# Fermeture de la fenêtre
				if event.type == pygame.QUIT:
					self.window_opened = False

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: # Clic gauche
						if self.focus:
							self.focus.remove_focus()
							self.focus = None
						for widget in self.widgets:
							if widget.check_coords(event.pos): # On regarde si le cliq est dans le bouton
								widget.action() # Exécution de l'action associée au bouton
								break

				elif event.type == pygame.KEYDOWN:
					if event.key in ARROW_KEYS:
						self.level.pacman.change_direction(ARROW_KEYS[event.key])

					else:
						if self.focus:
							self.focus.keydown(event)

			t2 = time.clock()

			tic_duration = t2 - t1 # Temps restant avant le rafraichissement de la fenêtre
			time_remaining = 0.06 - tic_duration

			if time_remaining > 0:
				time.sleep(time_remaining)

			pygame.display.flip() # Rafraichissement du rendu

		pygame.display.quit()

	def clear(self):
		self.widgets = []
		self.level = None
		self.focus = None
		self.container = None

	def focus_on(self, widget):
		self.focus = widget

	def close_window(self):
		self.window_opened = False

	def pause_game(self):
		self.game_running = False

	def start_game(self):
		self.game_running = True

	def add_widget(self, widget):
		self.widgets.append(widget)
