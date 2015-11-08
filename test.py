


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
