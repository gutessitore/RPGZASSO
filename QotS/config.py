# Configurações
import pygame as pg
import random 

# CORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (34, 165, 69)
RED = (255, 0, 0)
DARKRED = (165, 34, 34)
YELLOW = (255, 255, 0)
DARKYELLOW = (209, 209, 46)
BRIGHTYELLOW = (248, 249, 209)
BLUE = (100, 100, 255)
LIGHTBLUE = (68, 127, 221)

# game settings
WIDTH = 1542
HEIGHT = 800
WIDTH_FULL = 800
HEIGHT_FULL = 600
FPS = 60
TITLE = "Cthulhu Quest"
BGCOLOR = DARKGREEN


#config Monstro

MONSTRO_IMG = 'boar.png'
MONSTRO_SPEED = 250
MONSTRO_HIT_BOX = pg.Rect(0, 0, 58, 50)
MONSTRO_HEALTH = 250
DANO_MONSTRO = 20
MONTRO_PUSH = 20
MONSTRO_XP = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400


# config monstro_f
ELEMENT_IMG = 'elemental.png'
MONSTRO_F_SPEED = 150
MONSTRO_F_HIT_BOX = pg.Rect(0, 0, 46, 70)
MONSTRO_F_HEALTH = 270
DANO_MONSTRO_F = 45
MAGIA_F = 'Magia_Ent.png'
MONSTRO_F_XP = 40

#config monstro a

MONSTRO_A_SPEED = 25
MONSTRO_A_HIT_BOX = pg.Rect(0, 0, 46, 70)
MONSTRO_A_HEALTH = 450
DANO_MONSTRO_A = 40
MONSTRO_A_XP = 70

#config boss
BOSS_SPEED = 50
BOSS_HIT_BOX = pg.Rect(0, 0, 36, 60)
BOSS_HEALTH = 4000
DANO_BOSS = 100
BOSS_XP = 1000
MAGIA_B = 'boss_m.png'

#config jogador
VIDA = 500
PLAYER_SPEED = 200
BONECO = 'char.png'
PLAYER_HIT_BOX = pg.Rect(0, 0, 30, 40)
LVL_XP = 100

#Cajado
MAGIA_IMG = 'magia.png'
MAGIA_SPEED = 500
MAGIA_LIFETIME = 500
MAGIA_RATE = 150
ATK_DMG = 20
MANA = 200
SPIRIT = 100
SPIRIT_CUSTO = 15
MANA_CUSTO = 25
MANA_REGEN =0.5
MANA_CUSTO_ = 60

CUSTO_BOLADO = 100

#musicas
TELA_INICIAL = 'DF.png'
TELA_OVER = 'GO.png'
TELA_FINAL = 'final.png'
TELA_IN = 'historia.png'
TELA_INI = 'instru.png'
MUSICA_INICIAL = 'Overworld.ogg'
MUSICA_PRINCIPAL = 'boraBatalha.ogg'
FIREBALL = 'fireball.ogg'
WATERBALL = 'waterball.ogg'
SLIMEBALL = 'slimeball.ogg'
WOODBALL = 'woodball.ogg'
MAGIA_BOLADA = 'bolado.png'
MAD_TITAN = 'MT.png'

#spritesheet
SPRITESHEET_1 = 'chara7.png'
BOSS_IMG = 'BOSS.png'


CONTADOR = 0