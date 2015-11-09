import levels
import pygame
import constantes

""" Gestion du processus 'In Game' du jeu >BacMan the baccalaureates Adventure!< """

# class Game:
# 	def __init__(self):
# 		self.game_running = False # Indique que la boucle n'est pas encore lancée
# 		self.window_opened = True

# 		pygame.init()

# 		width = constantes.N_SQUARES_X * 16 * 2
# 		height = constantes.N_SQUARES_Y * 16 * 2

# 		window = pygame.display.set_mode((width, height))

# 		self.start()


########################
# Classes pour les cases
########################

class Square(object):
	def __init__(self):
		pass

	def render(self):
		pass

		## Rendu de la case

class EmptySquare(Square):
	def __init__(self):
		Square.__init__(self)
		self.is_empty = True # Le fantôme peut passer sur la case
		self.pill = False

class Wall(Square):
	def __init__(self):
		Square.__init__(self)
		self.is_empty = False # Le fantôme ne peut pas passer sur la case

###########################
# Classes pour les pillules
###########################

class Pill(EmptySquare): # Classe abstraite
	def __init__(self):
		EmptySquare.__init__(self)
		self.pill = True

	def eat(self):
		self.pill = False # La pillule n'est plus là
		self.picture = "" # Redevient une case vide

		self.effect()

class StandardPill(Pill):
	def __init__(self):
		Pill.__init__(self)
		self.points = 10
		self.picture = ""

	def effect(self):
		pass
		## Augmentation des points

class PowerPill(Pill):
	def __init__(self):
		Pill.__init__(self)
		self.picture = ""

	def effect():
		pass
		## Les fantômes s'arrêtent

class BonusPill(StandardPill):
	def __init__(self):
		Pill.__init__(self)

class Level:
	"""Classe permettant de créer un niveau"""

	# Définit les classes à utiliser pour les différents types de cases
	SQUARES = {
		"#" : Wall,
		"*" : StandardPill,
		"%" : PowerPill,
		"+" : BonusPill,
	}

	# CHARS = {
	# 	"p" : PacMan,
	# 	"B" : Blinky,
	# 	"P" : Pinky,
	# 	"I" : Inky,
	# 	"C" : Clyde,
	# }




	def __init__(self, n_level):

		self.level_filename = constantes.FILENAME_PATTERN.format(n_level)
		self.structure = []

		self.score = 0

	def parse(self):
		""" Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher."""

		### Penser à gérer les erreurs en cas d'anomalité dans le fichier de level

		# Ouverture du fichier
		level_file = open(self.level_filename, 'r')
		content = level_file.read()

		l_lines = content.split("\n")

		for line in l_lines:
			level_line = []
			square = None

			for char in line:
				if char in Level.SQUARES:
					square = Level.SQUARES[char]()

				elif char in Level.CHARS:
					### Instanciation du perso ici

					square = EmptySquare()

				else:
					pass ### Penser à lever une exception ici

				line_level.append(square) # La case es ajoutée à la ligne

			self.structure.append()

	def render(self):
		"""Réalise le rendu graphique de tous les éléments du jeu"""
		for line in self.structure :
			for square in line:
				square.render()

		### Rendu des personnages ici

	def prepare_pictures(self):
		self.wall = pygame.image.load("")


# class GameLoop:
# 	def __init__(self, master):
# 		self.window_opened = True
# 		self.game_running = False
# 		self.master = master

# 	def run_loop(self):
# 		while self.window_opened:
# 			if self.game_running:
# 				# le jeu tourne

# 			# Check pour la fermeture
# 			for event in pygame.event.get():
# 				if event.type == pygame.QUIT:
# 					self.window_opened = False

# 	def pause_game(self):
# 		self.game_running = False

# 	def start_game(self):
# 		self.game_running = True

##############################
# Classes pour les personnages
##############################

Game()

