# -*- coding: utf-8 -*-

import pygame as pg
import sys
from os import path
import settings
import sprites
import tilemap

class Combat:
    def __init__(self):
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption(settings.TITULO)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(200,100)
        self.load_data()
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.baus = pg.sprite.Group()
        self.player = pg.sprite.Group()
        for l in lista_baus:
            sprites.Bau(self, l[0], l[1], l[2], False)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    sprites.Wall(self, col, row)
                if tile == 'P':
                    self.player = sprites.Player(self, col, row)
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = tilemap.Map(path.join(game_folder, 'mapa_teste.txt'))###MUDAR PARA IMAGEM
        self.player_img = pg.image.load(path.join(img_folder, "char.png")).convert_alpha()###
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    def draw(self):
        self.screen.fill(settings.BG_COMBAT_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                    self.player.rot=180
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                    self.player.rot=0
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                    self.player.rot=90
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                    self.player.rot=270
                if event.key == pg.K_SPACE:
                    if self.player.rot == 0:
                        ver = [self.player.x+1, self.player.y]
                    elif self.player.rot == 90:
                        ver = [self.player.x, self.player.y-1]
                    elif self.player.rot == 180:
                        ver = [self.player.x-1, self.player.y]
                    elif self.player.rot == 270:
                        ver = [self.player.x, self.player.y+1]
                    for B in self.baus:
                        if B.x == ver[0] and B.y == ver[1]:
                            if B.aberto == False:
                                B.op = True
                                sprites.Bau(self, B.x, B.y, B.conteudo, B.op)
                                if B.conteudo not in self.player.inventario:
                                    self.player.inventario[B.conteudo]=1
                                else:
                                    self.player.inventario[B.conteudo]+=1
                                text_surface = settings.fonte.render("voce ganhou 1 {0}".format(B.conteudo), True, settings.BRANCO)
                                text_rect = text_surface.get_rect()
                                text_rect.midtop = (settings.WIDTH / 2,  3)
                                self.screen.blit(text_surface, text_rect)
                                #if event.key == pg.K_SPACE:


















