# Configurações
import pygame as pg

# CORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 100, 255)

# game settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Quest for the Swords"
BGCOLOR = DARKGREEN
FONT_NAME = 'arial'

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#config cenario

WALL_IMG = 'wall.png'
WALL_GRASS_IMG = 'grass_wall.png'


#config Monstros

MONSTRO_IMG = 'fantom.png'
MONSTRO_SPEED = 100
MONTRO_HIT_BOX = pg.Rect(0, 0, 50, 50)
MONSTRO_HEALTH = 200
DANO_MONSTRO = 15
MONTRO_PUSH = 20
AVOID_RADIUS = 50

#config jogador

VIDA = 500
PLAYER_SPEED = 200
BONECO = 'char.png'
PLAYER_HIT_BOX = pg.Rect(0, 0, 30, 40)

#Cajado
MAGIA_IMG = 'magia.png'
MAGIA_SPEED = 300
MAGIA_LIFETIME = 700
MAGIA_RATE = 200
ATK_DMG = 20


