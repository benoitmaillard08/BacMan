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

	def inputBox(self):
		"""
		inputBox() --> str pseudo
		Méthode recevant les entrées de l'utilisateur.
		"""
		entry = []
		ready = False

		while not ready:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if chr(event.key) in constantes.KEYS:
						entry += chr(event.key)

					elif event.key == 8: 	 # 8 --> code du backspace (pour effacer)
						if entry: 		# On vérifie si la liste n'est pas vide
							del entry[-1]

					elif event.key == 13:	 # 13 --> code du retour à la ligne (Enter)
						self.pseudo = compiler(entry)
						ready = True

					else:
						# Indique à l'utilisateur que le caractère entré n'est pas autorisé.
						pass





