import pygame
import constantes

def load_terrain(filename):
	return pygame.image.load(constantes.TERRAIN_DIR + filename + ".gif")

