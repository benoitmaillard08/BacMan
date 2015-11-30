import pygame
from pygame.locals import *
import constantes



class Test:
    
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((constantes.COTE_FOND, constantes.COTE_FOND), RESIZABLE)

        #Chargement du fond
        background = pygame.image.load(constantes.PATH_PIC_PAGES)
        self.window.blit(background, (0,0))

        #Mise à jour de la page
        pygame.display.flip()
    def compiler(self, liste):
        """
        compile( list liste) --> str
    Méthode permettant de compiler la liste de charactères entrés en string."""
        string = ''

        for elt in liste:
            string += elt

        return string

    def events(self):
            
        #Gestionnaire d'événements
        liste = []

        while 1:
            for event in pygame.event.get():    # Parcours la liste des éléments reçus
                if event.type == QUIT:
                    flag = 0
                    
                elif event.type == KEYDOWN:
                    if chr(event.key) in constantes.KEYS:
                        liste += chr(event.key)
                        print(Test().compiler(liste))
                        
                    elif event.key == 8:    # 8 --> code du backspace (pour effacer)
                        if liste:   # On vérifie si la liste est vide, si oui, on ne fait rien
                            del liste[-1]
                            print(Test().compiler(liste))
                            
                        
                    elif event.key == 13:       # 13 --> code du retour à la ligne (Enter)
                        pseudo = ''
                        for elt in liste:
                            pseudo += elt
                        print(Test().compiler(liste))
                        
                    else:
                        print('Seuls les caractères normaux et sans accent sont acceptés!')
                    
                    
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x = event.pos[0]    #Les positions du clic de la souris sont enregistrés pour être analyser
                    y = event.pos[1]
                
        pygame.display.quit()

Test().compiler([])
Test().events()




        
    

        
    
