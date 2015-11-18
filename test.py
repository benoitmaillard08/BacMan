import pygame
from pygame.locals import *
import constantes

pygame.init()

continuer = 1

window = pygame.display.set_mode((800, 800), RESIZABLE)

background = pygame.image.load(constantes.PATH_PIC_MAIN_MENU).convert()
window.blit(background,(0,0))


text_to_display = open(constantes.RULES_TEXT, 'r').readlines()
line = 50
font = pygame.font.Font('ressources/monofonto.ttf', constantes.TEXTFONT_SIZE)
text = font.render(text_to_display[0], 1, (255,255,255))
window.blit(text, (10,10))
i  = 0
while i < len(text_to_display):
	text = font.render(text_to_display[i], 1, constantes.RGB_WHITE)
	print(text_to_display[i])
	background.blit(text, (line, 25)) # 'Collage' de la ligne, avec 25 pixels de marge à gauche
	pygame.display.flip()
	line += constantes.TEXTFONT_SIZE + 10  #La position de la prochaine ligne est placée à 25 + 10 pixels plus bas
	i += 1

pygame.display.flip()

while continuer:
	for event in pygame.event.get():    # On parcourt la liste de tous les événements reçus
		if event.type == QUIT:    #Si l'un de ces événement est de type QUIT
			continuer = 0

pygame.display.quit()
