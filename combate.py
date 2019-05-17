# -*- coding: utf-8 -*-

import pygame as pg
import sys
from os import path
import settings
import sprites
import tilemap

class Combat:
    def __init__(self, screen):
        self.run()
        self.screen = screen
 
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.baus = pg.sprite.Group()
        self.player = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    sprites.Wall(self, col, row)
                if tile == 'P':
                    self.player = sprites.Player(self, col, row)
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = tilemap.Map(path.join(game_folder, 'mapa_teste.txt'))###MUDAR PARA IMAGEM
        self.player_img = pg.image.load(path.join(img_folder, "char.png")).convert_alpha()###

    def run(self):
        # game loop - set self.playing = False to end the game
        self.combat = True
        while self.combat:
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
        
    def draw(self):
        self.screen.fill(settings.BG_COMBAT_COLOR)
        pg.display.flip()
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        # catch all events here//
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_a:
                    self.player.move(dx=-1)
                    self.player.rot=180
                if event.key == pg.K_i:
                    self.player.move(dx=1)
                    self.player.rot=0
                if event.key == pg.K_f:
                    self.player.move(dy=-1)
                    self.player.rot=90
                if event.key == pg.K_t:
                    self.player.move(dy=1)
                    self.player.rot=270
                


















