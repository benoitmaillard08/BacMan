import levels
import pygame
import constantes

""" Gestion du processus 'In Game' du jeu >BacMan the baccalaureates Adventure!< """

class Game:
	def __init__(self):
		self.game_running = False # Indique que la boucle n'est pas encore lancé
		self.window_opened = True

		pygame.init()

		width = constantes.N_SQUARES_X * 16 * 2
		height = constantes.N_SQUARES_Y * 16 * 2

		window = pygame.display.set_mode((width, height))

		self.start()


	def pause(self):
		pass

	def start(self):
		self.game_running = True
		
		self.loop()

	def loop(self):
		while self.window_opened:
			# if self.game_running:
				# le jeu tourne

			# Check pour la fermeture
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.window_opened = False

Game()

