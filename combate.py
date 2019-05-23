# -*- coding: utf-8 -*-

import pygame as pg
import sys
from os import path
import settings
import sprites
import tilemap
import random

class Combate_central:
    def __init__(self, screen, all_sprites, camera, player, mato):
        self.new()
        self.screen = screen
        self.all_sprites = all_sprites
        self.camera = camera
        self.player = player
        self.condicao = 'escolha'
        self.criaturaP = player.party[0]
        monstro = random.choice(mato.monstros)
        mvset = []
        while len(mvset)<4:
            nmv = random.choice(monstro.move_pool)
            if nmv not in mvset:
                mvset.append(nmv)
        self.adversario = sprites.Criatura(mvset, random.randint(mato.lvmin,mato.lvmax+1),0,monstro)
        

    def new(self):
        # initialize all variables and do all the setup for a new game
        pass
    
    def load_data(self):
        pass
        """
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = tilemap.Map(path.join(game_folder, 'mapa_teste.txt'))###MUDAR PARA IMAGEM
        self.player_img = pg.image.load(path.join(img_folder, "char.png")).convert_alpha()###"""

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
    def goback(self):
        self.combat = False
    def draw(self):
        self.screen.fill(settings.BG_COMBAT_COLOR)
        if self.condicao == 'escolha':
            pg.draw.rect(self.screen, settings.BEJE,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
            
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6/5-16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6/5-16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
 
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6/5-12, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6/5-12, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
        if self.condicao == 'combate':
            pg.draw.rect(self.screen, settings.BEJE,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
            
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6/5-16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6/5-16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
            pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
 
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6/5-12, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6/5-12, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            
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
                if self.condicao == 'escolha':
                    if event.key == pg.K_a:
                        self.condicao = 'combate'
                    if event.key == pg.K_i:
                        self.condicao = 'item'
                    if event.key == pg.K_f:
                        self.condicao = 'fugir'
                    if event.key == pg.K_t:
                        self.condicao = 'trocar'
                    if event.key == pg.K_SPACE:
                        self.goback()




















