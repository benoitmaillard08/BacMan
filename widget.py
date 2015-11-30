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






