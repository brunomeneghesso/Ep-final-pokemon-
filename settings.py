import pygame as pg
from os import path
pg.font.init()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_ESC = (40, 40, 40)
CINZA_CLA = (100, 100, 100)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AMARELO_ESC = (200,150,0)

# game settings
WIDTH = 1056   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 800  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITULO = "EP pré-alfa"
BGCOLOR = CINZA_ESC
BG_COMBAT_COLOR = PRETO

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

fnt_dir = path.join(path.dirname(__file__), 'fnt')
fonte = pg.font.Font(path.join(fnt_dir, "Cardinal.ttf"), 28)