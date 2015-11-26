import pygame
from pygame.locals import *
import constantes
from tkinter import *


class Window(Tk):
    def __init__(self):
        window = Tk()

class Test:
    
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((constantes.COTE_FOND, constantes.COTE_FOND), RESIZABLE)

        #Chargement du fond
        background = pygame.image.load(constantes.PATH_PIC_PAGES)
        self.window.blit(background, (0,0))

        #Mise à jour de la page
        pygame.display.flip()

        #Gestionnaire d'événements
        flag = 1
        print('{', end='')

        while flag:
            for event in pygame.event.get():    # Parcours la liste des éléments reçus
                if event.type == QUIT:
                    flag = 0
                    
                elif event.type == KEYDOWN:
                    print('K_'+chr(event.key)+':"'+chr(event.key)+'"', end=',')
                    
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x = event.pos[0]    #Les positions du clic de la souris sont enregistrés pour être analyser
                    y = event.pos[1]
                
        print('}', end='\n')
        pygame.display.quit()




        
    

        
    
