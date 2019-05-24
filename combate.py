# -*- coding: utf-8 -*-

import pygame as pg
import sys
from os import path
import settings
import sprites
import tilemap
import random

class Combate_central:
    def __init__(self, game, screen, all_sprites, camera, player, mato):
        self.new()
        self.game = game
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
            
            text_surface = self.game.font20.render("A", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6/5-8)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font.render("Atacar", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6/5+8)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font20.render("I", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6/5-8)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font.render("Item", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6/5+8)
            self.screen.blit(text_surface, text_rect)

            text_surface = self.game.font20.render("F", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font.render("Fugir", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font20.render("T", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font.render("Trocar", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
            self.screen.blit(text_surface, text_rect)
            
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
            
            text_surface = self.game.font20.render("Q", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6/5-8)
            self.screen.blit(text_surface, text_rect)
            
            text_surface = self.game.font.render(self.criaturaP.moves[0].nome, True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6/5+8)
            self.screen.blit(text_surface, text_rect)
            
            if len(self.criaturaP.moves)>=2:
                text_surface = self.game.font20.render("W", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6/5-8)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render(self.criaturaP.moves[1].nome, True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6/5+8)
                self.screen.blit(text_surface, text_rect)

            if len(self.criaturaP.moves)>=3:
                text_surface = self.game.font20.render("E", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render(self.criaturaP.moves[2].nome, True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
            
            if len(self.criaturaP.moves)>=4:
                text_surface = self.game.font20.render("R", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render(self.criaturaP.moves[3].nome, True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
            
        pg.display.flip()
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def atacar(self,golpe):
        c=0
        while c<3:
            M = self.criaturaP.monstro
            lvp = self.criaturaP.lv
            A = self.adversario.monstro
            lva = self.adversario.lv
            dano = golpe.dano*(M.atk+M.ganho[0]*(lvp-1)) - (A.df+A.crescimento*(lva-1))
            if dano>0:
                self.adversario.sofre_dano(dano)
                
        
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
                if self.condicao == 'combate':
                    if event.key == pg.K_q:
                        
                    if event.key == pg.K_w:
                        
                    if event.key == pg.K_e:
                        
                    if event.key == pg.K_r:
                        
                    if event.key == pg.K_SPACE:
                        self.condicao = 'escolha'
                        
