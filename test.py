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

    
    def display_box(self, text):

        button = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()
        self.window.blit(button, (200,400))

        font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.MENUFONT_SIZE )
        text = font.render(text, 0, (255,255,255))

        self.window.blit(text, (300,400))

        pygame.display.flip()


        

    def events(self):
            
        #Gestionnaire d'événements
        liste = []

        while 1:
            for event in pygame.event.get():    # Parcours la liste des éléments reçus
                if event.type == QUIT:
                    break
                    
                elif event.type == KEYDOWN:
                    if chr(event.key) in constantes.KEYS:
                        Test.__init__(self)
                        liste += chr(event.key)
                        Test.display_box(self, Test.compiler(self,liste))
                        
                    elif event.key == 8:    # 8 --> code du backspace (pour effacer)
                        if liste:   # On vérifie si la liste est vide, si oui, on ne fait rien
                            del liste[-1]
                            Test.__init__(self)
                            Test.display_box(self, Test.compiler(self,liste))
                            
                    elif event.key == 13:       # 13 --> code du retour à la ligne (Enter)
                        pseudo = ''
                        Test.__init__(self)
                        for elt in liste:
                            pseudo += elt
                        Test.display_box(self, Test.compiler(self,liste))
                        
                    else:
                        print('Seuls les caractères normaux et sans accent sont acceptés!')
                    
                    
    
        pygame.display.quit()



                
        

Test().compiler([])
Test().events()
    





        
    

        
    
