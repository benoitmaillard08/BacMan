import pygame
import constantes

def load_terrain(filename):
	surface = pygame.image.load(constantes.TERRAIN_DIR + filename + ".gif").convert_alpha()
	return pygame.transform.scale(surface, (constantes.SQUARE_SIZE, constantes.SQUARE_SIZE))

def load_sound(filename):
	sound = pygame.mixer.Sound(constantes.SOUND_DIR + filename + ".wav")
	return sound