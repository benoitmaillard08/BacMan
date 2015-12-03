import pygame
from pygame.locals import *
import constantes



class Test:
    
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((constantes.WINDOW_X, constantes.WINDOW_Y), RESIZABLE)

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

    
    def display_box(self):

        button = pygame.image.load(constantes.PATH_PIC_BUTTON).convert_alpha()
        self.window.blit(button, (200,400))

        pygame.display.flip()
        
    def display_text(self, text):
        
        font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.TEXTFONT_SIZE )
        size = font.size(text)[0]
        text_to_display = font.render(text, 0, (255,255,255))

        self.window.blit(text_to_display, (self.window.get_width()//2 - size//2,410))

        pygame.display.flip()


        

    def events(self, maxCar=15):
            
        #Gestionnaire d'événements
        self.liste = []
        Test.display_box(self)
        pageRunning=True
        while pageRunning:
            
            for event in pygame.event.get():    # Parcours la liste des éléments reçus
                
                if event.type == QUIT:
                    pageRunning = False
                    
                elif event.type == KEYDOWN:
                    Test.__init__(self)
                    Test.display_box(self)
                    if chr(event.key) in constantes.KEYS and len(self.liste)<=maxCar:
                        self.liste += chr(event.key)
       
                    elif event.key == 8:    # 8 --> code du backspace (pour effacer)
                        if self.liste:   # On vérifie si la liste est vide, si oui, on ne fait rien
                            del self.liste[-1]
  
                    elif event.key == 13:       # 13 --> code du retour à la ligne (Enter)
                        pseudo = ''
                        for elt in self.liste:
                            pseudo += elt

                    elif not len(self.liste) <= maxCar:
                        print('Le nombre maximum de caractères est de',maxCar)

                    else:
                        print('Seuls les caractères normaux et sans accent sont acceptés!')

                    Test.display_text(self, Test.compiler(self,self.liste))
                    
    
        pygame.display.quit()



                
        

Test().compiler([])
Test().events()
    





        
    

        
    
