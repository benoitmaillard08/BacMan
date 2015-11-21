"""Liste des constantes du jeu >BacMan the baccalaureates Adventure!<"""

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
PATH_PIC_BUTTON = "ressources/button.png2"

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
N_SQUARES_Y = 28

PIC_DIR = "ressources/pictures/"

GAME_BACKGROUND = "background/bg.gif"
TERRAIN_DIR = PIC_DIR + "terrain/"
TEXT_DIR = PIC_DIR + "text/"

FILENAME_PATTERN = "n{}.level"

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
