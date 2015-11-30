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
COTE_FOND = 800 #pixels
PATH_PIC_MAIN_MENU = "ressources/main_menu.png"
PATH_PIC_BUTTON = "ressources/button.png"

####Pages####
PATH_PIC_PAGES = "ressources/pages_bg.png"

#Règles
RULES_TITLE = 'Reglement'
RULES_TEXT = 'ressources/rules.txt'

#Contrôles
CTRLS_TEXT = ['Contrôles =','Pause =', 'Quitter =']
CTRLS_PIC_DIR = ['ressources/arrow_keys.png','ressources/p_key.png','ressources/esc_key.png']
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
# Dictionnaire des constantes pygame avec leurs lettres/chiffres correspondants

#KEYS = {"K_1":"1","K_2":"2","K_3":"3","K_4":"4","K_5":"5","K_6":"6","K_7":"7","K_8":"8","K_9":"9","K_0":"0",
#		"K_q":"q","K_w":"w","K_e":"e","K_r":"r","K_t":"t","K_y":"y","K_u":"u","K_i":"i","K_o":"o","K_p":"p",
#		"K_a":"a","K_s":"s","K_d":"d","K_f":"f","K_g":"g","K_h":"h","K_j":"j","K_k":"k","K_l":"l","K_z":"z",
#		"K_x":"x","K_c":"c","K_v":"v","K_b":"b","K_n":"n","K_m":"m"}

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