"""Liste des constantes du jeu >BacMan the baccalaureates Adventure!<"""

import pygame

# Type de case
WALL = "#"
STANDARD_PILL = "*"
POWER_PILL = "P"
BONUS_PILL = "B"
#=======




#------------------------------------------------------------
# Menu
WINDOW_X = 800 #pixels
WINDOW_Y = 800
PATH_PIC_MAIN_MENU = "ressources/main_menu.png"
PATH_PIC_BUTTON = "ressources/button_2.png"

####Pages####
PATH_PIC_PAGES = "ressources/pages_bg.png"

#Règles
RULES_TITLE = 'Reglement'
RULES_TEXT = 'ressources/rules.txt'

#Contrôles
CTRLS_TEXT = ['Contrôles =','Pause =', 'Quitter =']
CTRLS_PIC_DIR = ['ressources/arrow_keys.png','ressources/p_key.png','ressources/esc_key.png']
#############

# Base(s) de données

PLAYERS_DATAS = 'players.txt'



#############




#Postions boutons (Tuples)
POS_BUT = (100, 400)

# Chemin Police
MENUFONT_DIR = "ressources/8bit_font.ttf"
TEXTFONT_DIR = "ressources/monofonto.ttf"

MENUFONT_SIZE = 40 #pixels
TEXTFONT_SIZE = 25

# Couleurs (Tuples)
RGB_WHITE = (255,255,255)  # Le RGBA du blanc = (255,255,255), du noir (0,0,0)
RGB_BLACK = (0,0,0)


#------------------------------------------------------------

N_SQUARES_X = 28
N_SQUARES_Y = 20

PIC_DIR = "ressources/pictures/"

GAME_BACKGROUND = PIC_DIR + "background/bg.gif"
TERRAIN_DIR = PIC_DIR + "terrain/"
TEXT_DIR = PIC_DIR + "text/"

LEVELS_DIR = "levels/"

FILENAME_PATTERN = "n{}.level"
WALLS_PATTERN = "wall-{}"
PACMAN_PATTERN = "pacman-{} {}"
FRUIT_PATTERN = "fruit {}"
GHOST_PATTERN = "ghost {}"

#-----------------------------------

# Différents types de cases

WALL = "#"

PILL = "*"
POWER_PILL = "%"
BONUS_PILL = "+"

PACMAN = "p"
BLINKY = "B"
PINKY = "P"
INKY = "I"
CLYDE = "C"

SQUARE_SIZE = 32

DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))


# ---------------------------------------
# Liste des caractères utilisables pour les pseudos et mots de passe

KEYS = ['1','2','3','4','5','6','7','8','9','0',
		'q','w','e','r','t','y','u','i','o','p',
		'a','s','d','f','g','h','j','k','l','z',
		'x','c','v','b','n','m',]


ARROW_KEYS = {
	pygame.K_UP : 0,
	pygame.K_RIGHT : 1,
	pygame.K_DOWN : 2,
	pygame.K_LEFT : 3,
}