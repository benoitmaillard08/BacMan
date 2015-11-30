class Loop:
	def __init__(self, level=None):
		self.window_opened = True
		self.game_running = False
		self.level = level

		self.buttons = [] # Boutons présents sur la page
		self.text_areas = [] # Zones de texte sur la page

	def run_loop(self):
		while self.window_opened:
			t1 = time.clock()

			if self.level:
				self.level.game_tic()

			# Check pour la fermeture
			for event in pygame.event.get():
				# Fermeture de la fenêtre
				if event.type == pygame.QUIT:
					self.window_opened = False

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: # Cliq gauche
						for button in self.buttons:
							if button.check_coords(event.pos): # On regarde si le cliq est dans le bouton
								button.action() # Exécution de l'action associée au bouton
								break

				elif event.type == pygame.KEYDOWN:
					if event.key in ARROW_KEYS:
						self.level.pacman.change_direction(ARROW_KEYS[event.key])

			t2 = time.clock()

			print(t2-t1)

			time.sleep(0.06 - (t2 - t1))



	def pause_game(self):
		self.game_running = False

	def start_game(self):
		self.game_running = True

	def add_button(self, button):
		self.buttons.append(button)

	def add_text_area(self, area):
		self.text_areas.append(area)