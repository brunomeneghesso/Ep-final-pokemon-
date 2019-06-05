# -*- coding: utf-8 -*-

import pygame as pg
import sys
import settings
import sprites
import random
from os import path


class Combate_central:
    def __init__(self, game, screen, all_sprites, camera, player, mato):
        self.game = game
        self.screen = screen
        self.all_sprites = all_sprites
        self.camera = camera
        self.player = player
        self.condicao = 'escolha'
        self.criaturaP = player.party[0]
        self.c = 0 
        self.disponivel = 0
        for d in self.player.party:
            if d.hp > 0:
                self.disponivel+=1
        monstro = random.choice(mato.monstros) 
        mvset = []
        lv = random.randint(mato.lvmin,mato.lvmax+1)
        possiveis=[]
        for m,nv in monstro.move_pool.items():
            if nv<=lv:
                possiveis.append(m)
        if len (possiveis) > 4:
            while len(mvset)<4:
                nmv = random.choice(monstro.move_pool)
                if nmv not in mvset:
                    mvset.append(nmv)
        else:
            mvset = possiveis
        self.adversario = sprites.Criatura(mvset, lv,0,monstro)
        self.M = self.criaturaP.monstro
        self.lvp = self.criaturaP.lv
        self.A = self.adversario.monstro
        self.lva = self.adversario.lv
        self.golpe = ''
        self.T=True
        self.vida=self.criaturaP.hp
        self.vidaA=self.adversario.hp
        self.mana=self.criaturaP.mana
        self.manaA=self.adversario.mana
        self.capturou = 'O adversário está se dissipando em energia, gostaria de sela-lo?'
        self.lista_itens=[]
        for i in self.player.inventario.keys():
            if i != 'selo de captura':
                self.lista_itens.append(i)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Textures')
        self.combat_back = pg.image.load(path.join(img_folder, "combat_background.png")).convert()

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
    def forcegoback(self):
        self.combat = False
    def draw(self):
        self.screen.fill(settings.BG_COMBAT_COLOR)
        background_combat = sprites.Background_combat (self, [0,0])
        self.screen.blit(background_combat.image, background_combat.rect)
        imgP=self.M.image1
        rectP=self.M.rect1
        rectP.left , rectP.top = [settings.WIDTH/8, settings.HEIGHT/4] 
        self.screen.blit(imgP, rectP)
        
        imgA=self.A.image2
        rectA=self.A.rect2
        rectA.left , rectA.top = [settings.WIDTH*5/8, settings.HEIGHT/4] 
        self.screen.blit(imgA, rectA)
        
        pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/8,settings.HEIGHT/9-24,settings.WIDTH/4,44])
        pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH*5/8,settings.HEIGHT/9-24,settings.WIDTH/4,44])
        
        text_surface = self.game.font40.render(str(self.M.nome), True, settings.PRETO)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (settings.WIDTH/8, settings.HEIGHT/9-24)
        self.screen.blit(text_surface, text_rect)
        
        text_surface = self.game.font40.render(str(self.A.nome), True, settings.PRETO)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (settings.WIDTH*5/8, settings.HEIGHT/9-24)
        self.screen.blit(text_surface, text_rect)
        if self.vida>self.criaturaP.hp:
            self.vida-=0.5
        if self.vidaA>self.adversario.hp:
            self.vidaA-=0.5
        if self.mana>self.criaturaP.mana:
            self.mana-=0.5
        if self.manaA>self.adversario.mana:
            self.manaA-=0.5
        x=(settings.WIDTH/4-8)*self.vida/self.criaturaP.hpmax
        y=(settings.WIDTH/4-8)*self.vidaA/self.adversario.hpmax
        X=(settings.WIDTH/4-8)*self.mana/self.criaturaP.manamax
        Y=(settings.WIDTH/4-8)*self.manaA/self.adversario.manamax
        pg.draw.rect(self.screen, settings.VERMELHO,[settings.WIDTH/8+4,settings.HEIGHT/9-20,x,24])
        pg.draw.rect(self.screen, settings.VERMELHO,[settings.WIDTH*5/8+4,settings.HEIGHT/9-20,y,24])
        pg.draw.rect(self.screen, settings.AZUL,[settings.WIDTH/8+4,settings.HEIGHT/9+8,X,8])
        pg.draw.rect(self.screen, settings.AZUL,[settings.WIDTH*5/8+4,settings.HEIGHT/9+8,Y,8])
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
            
            text_surface = self.game.font20.render(str(self.criaturaP.moves[0].custo), True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.bottomright = (settings.WIDTH/2-28, settings.HEIGHT*5/6-20)
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
                
                text_surface = self.game.font20.render(str(self.criaturaP.moves[1].custo), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.bottomright = (settings.WIDTH*9/10+4, settings.HEIGHT*5/6-20)
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
                
                text_surface = self.game.font20.render(str(self.criaturaP.moves[2].custo), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.bottomright = (settings.WIDTH/2-28, settings.HEIGHT*29/30+12)
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
            
                text_surface = self.game.font20.render(str(self.criaturaP.moves[3].custo), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.bottomright = (settings.WIDTH*9/10+4, settings.HEIGHT*29/30+12)
                self.screen.blit(text_surface, text_rect)
        if self.condicao == 'atacando':
            if self.c == 0:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                text_surface = self.game.font40.render("{0} atacou o {1} adversário com {2}".format(self.M.nome, self.A.nome, self.golpe.nome), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
            
            if self.c == 1:
                ef=0
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                for T in self.adversario.monstro.tipo:
                    if self.golpe.tipo in T.fraquesa:
                        ef+=1
                    elif self.golpe.tipo in T.resistencia:
                        ef-=1
                if ef>0:
                    text_surface = self.game.font.render("Foi super efetivo!", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
                elif ef<0:
                    text_surface = self.game.font.render("Foi pouco efetivo", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
                else:
                    text_surface = self.game.font.render("Dano elemental neutro", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
        if self.condicao == 'atacado':
            if self.c == 1:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                text_surface = self.game.font.render("{0} atacou seu {1} com {2}".format(self.A.nome, self.M.nome, self.golpe.nome), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)

            if self.c == 2:
                ef=0
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                for T in self.criaturaP.monstro.tipo:
                    if self.golpe.tipo in T.fraquesa:
                        ef+=1
                    elif self.golpe.tipo in T.resistencia:
                        ef-=1
                if ef>0:
                    text_surface = self.game.font.render("Foi super efetivo!", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
                elif ef<0:
                    text_surface = self.game.font.render("Foi pouco efetivo", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
                else:
                    text_surface = self.game.font.render("Dano elemental neutro", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
        if self.condicao == 'falhou fugir':
            pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
            text_surface = self.game.font.render("Você não conseguiu fugir, o inimigo foi mais rápido!", True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
            self.screen.blit(text_surface, text_rect)
        if self.condicao == 'fugir':
            self.goback()
        if self.condicao == 'ganhou':
            if self.c == 0:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                text_surface = self.game.font40.render("Você derrotou o adversário!", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
            
            if self.c == 1:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                exp=int(self.criaturaP.lv/self.adversario.lv*10)
                text_surface = self.game.font40.render("Seu {0} ganhou {1} de experiência, que bom!".format(self.M.nome, exp), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
        if self.condicao == 'perdeu':
            pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])

            text_surface = self.game.font40.render("O inimigo derrotou seu {0}.".format(self.M.nome), True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
            self.screen.blit(text_surface, text_rect)
        
        if self.condicao == 'trocar':
            if self.disponivel >= 1:
                pg.draw.rect(self.screen, settings.BEJE,[0, 0, settings.WIDTH, settings.HEIGHT])
                
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, 32, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, 32, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, (settings.HEIGHT-160)/4+64, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, (settings.HEIGHT-160)/4+64, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, (settings.HEIGHT-160)/2+96, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, (settings.HEIGHT-160)/2+96, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, (settings.HEIGHT-160)*3/4+128, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, (settings.HEIGHT-160)*3/4+128, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])

     
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, 36, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, 36, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, (settings.HEIGHT-160)/4+68, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, (settings.HEIGHT-160)/4+68, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, (settings.HEIGHT-160)/2+100, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, (settings.HEIGHT-160)/2+100, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, (settings.HEIGHT-160)*3/4+132, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, (settings.HEIGHT-160)*3/4+132, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                
                X=0
                pos = [[settings.WIDTH*3/10-20,(settings.HEIGHT-160)/8+32],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)/8+32],[settings.WIDTH*3/10-20,(settings.HEIGHT-160)*3/8+64],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)*3/8+64],[settings.WIDTH*3/10-20,(settings.HEIGHT-160)*5/8+96],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)*5/8+96],[settings.WIDTH*3/10-20,(settings.HEIGHT-160)*7/8+128],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)*7/8+128]]
                for p in self.player.party:
                    if p.hp>0:
                        text_surface = self.game.font20.render("{0}".format(X+1), True, settings.BRANCO)
                        text_rect = text_surface.get_rect()
                        text_rect.center = (pos[X][0]-(settings.WIDTH/5-20),pos[X][1]-((settings.HEIGHT-160)/8-24))
                        self.screen.blit(text_surface, text_rect)
                        text_surface = self.game.font40.render("{0}".format(p.monstro.nome), True, settings.BRANCO)
                    else:
                        text_surface = self.game.font40.render("{0}".format(p.monstro.nome), True, settings.CINZA_CLA)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0],pos[X][1])
                    self.screen.blit(text_surface, text_rect)
                    X+=1
            else:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])

                text_surface = self.game.font40.render("Você não tem mais monstros para lutar por ao seu lado.", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
        if self.condicao == 'captura':
            if self.c == 0:
                pg.draw.rect(self.screen, settings.BEJE,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
               
                text_surface = self.game.font.render(self.capturou, True, settings.PRETO)
                text_rect = text_surface.get_rect()
                text_rect.center = (settings.WIDTH / 2,  settings.HEIGHT *9 / 12)
                self.screen.blit(text_surface, text_rect)
                
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
                
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            
                text_surface = self.game.font20.render("S", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
            
                text_surface = self.game.font.render("Sim!", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font20.render("N", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render("Não", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
            
            if self.c == 1:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                text_surface = self.game.font.render("Você usou um selo de captura, aida tem mais{0}".format(self.player.inventario['selo de captura']), True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
            if self.c == 2:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                text_surface = self.game.font.render(self.capturou, True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
            if self.c == 3:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                text_surface = self.game.font.render("Você não tem mais espaço nos seus pergaminhos", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
            
            if self.c == 4:
                pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                
                text_surface = self.game.font.render("A criatura está no seu morelo", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                self.screen.blit(text_surface, text_rect)
        if self.condicao == 'item':
            if self.disponivel >= 1:
                pg.draw.rect(self.screen, settings.BEJE,[0, 0, settings.WIDTH, settings.HEIGHT])
                
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, 32, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, 32, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, (settings.HEIGHT-160)/4+64, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, (settings.HEIGHT-160)/4+64, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, (settings.HEIGHT-160)/2+96, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, (settings.HEIGHT-160)/2+96, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, (settings.HEIGHT-160)*3/4+128, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, (settings.HEIGHT-160)*3/4+128, settings.WIDTH*2/5, (settings.HEIGHT-160)/4])

     
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, 36, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, 36, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, (settings.HEIGHT-160)/4+68, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, (settings.HEIGHT-160)/4+68, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, (settings.HEIGHT-160)/2+100, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, (settings.HEIGHT-160)/2+100, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, (settings.HEIGHT-160)*3/4+132, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, (settings.HEIGHT-160)*3/4+132, settings.WIDTH*2/5-8, (settings.HEIGHT-160)/4-8])
                
                X=0
                pos = [[settings.WIDTH*3/10-20,(settings.HEIGHT-160)/8+32],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)/8+32],[settings.WIDTH*3/10-20,(settings.HEIGHT-160)*3/8+64],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)*3/8+64],[settings.WIDTH*3/10-20,(settings.HEIGHT-160)*5/8+96],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)*5/8+96],[settings.WIDTH*3/10-20,(settings.HEIGHT-160)*7/8+128],[settings.WIDTH*7/10+6,(settings.HEIGHT-160)*7/8+128]]
                for i in self.lista_itens:
                    text_surface = self.game.font20.render("{0}".format(X+1), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0]-(settings.WIDTH/5-20),pos[X][1]-((settings.HEIGHT-160)/8-24))
                    self.screen.blit(text_surface, text_rect)
                    text_surface = self.game.font40.render("{0}".format(i.nome), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0]-64,pos[X][1])
                    self.screen.blit(text_surface, text_rect)
                    text_surface = self.game.font40.render("{0}".format(self.player.inventario[i]), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0]+128,pos[X][1])
                    self.screen.blit(text_surface, text_rect)
                    X+=1
            if self.condicao == 'subiu nivel':
                if self.c == 0:
                    pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
        
                    text_surface = self.game.font40.render("{0} subiu para o nivel.{1}".format(self.M.nome,self.criaturaP.lv), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
                if self.c == 1:
                    pg.draw.rect(self.screen, settings.BEJE,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                   
                    text_surface = self.game.font.render("Quer ensinar {0} a como usar {1}".format(self.M.nome,self.golpe.nome), True, settings.PRETO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (settings.WIDTH / 2,  settings.HEIGHT *9 / 12)
                    self.screen.blit(text_surface, text_rect)
                    
                    pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
                    pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
                    
                    pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
                    pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
                
                    text_surface = self.game.font20.render("S", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                    self.screen.blit(text_surface, text_rect)
                
                    text_surface = self.game.font.render("Sim!", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                    self.screen.blit(text_surface, text_rect)
                    
                    text_surface = self.game.font20.render("N", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                    self.screen.blit(text_surface, text_rect)
                    
                    text_surface = self.game.font.render("Não", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                    self.screen.blit(text_surface, text_rect)
                if self.c == 2:
                    pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
        
                    text_surface = self.game.font40.render("Selecione um golpe para ser substituido", True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *8 / 10)
                    self.screen.blit(text_surface, text_rect)
                if self.c == 3:
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
                
                text_surface = self.game.font.render(self.criaturaP.moves[0], True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6/5+8)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font20.render("W", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6/5-8)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render(self.criaturaP.moves[1], True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6/5+8)
                self.screen.blit(text_surface, text_rect)
    
                text_surface = self.game.font20.render("E", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render(self.criaturaP.moves[2], True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font20.render("R", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
                
                text_surface = self.game.font.render(self.criaturaP.moves[3], True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
        pg.display.flip()
    def goback(self):
        ASD = random.randint(0,100)
        if ASD < 76:
            self.combat = False
        else:
            self.condicao = "falhou fugir"
    def update(self):
        self.all_sprites.update()
    def atacar(self):
        dano = self.golpe.dano*(self.M.atk+self.M.crescimento[0]*(self.lvp-1)) - (self.A.df+self.A.crescimento[0]*(self.lva-1))
        self.criaturaP.mana-=self.golpe.custo
        if self.criaturaP.mana<0:
            self.criaturaP.sofre_dano(-self.criaturaP.mana)
            self.criaturaP.mana=0
        for T in self.A.tipo:
            if self.golpe.tipo in T.fraquesa:
                dano = dano*2
            elif self.golpe.tipo in T.resistencia:
                dano = int(dano/2)
        for T in self.M.tipo:
            if self.golpe.tipo == T:
                dano = dano*2
        self.adversario.sofre_dano(dano)
    def atacado(self):
        self.c=0
        self.golpe=random.choice(self.adversario.moves)
        self.adversario.mana-=self.golpe.custo
        if self.adversario.mana<0:
            self.adversario.sofre_dano(-self.criaturaP.mana)
            self.adversario.mana=0
        dano = self.golpe.dano*(self.A.atk+self.A.crescimento[0]*(self.lva-1)) - (self.M.df+self.M.crescimento[0]*(self.lvp-1))
        for T in self.M.tipo:
            if self.golpe.tipo.nome in T.fraquesa:
                dano = dano*2
            elif self.golpe.tipo.nome in T.resistencia:
                dano = int(dano/2)
        for T in self.A.tipo:
            if self.golpe.tipo == T:
                dano = dano*2
        if dano>0:
            self.criaturaP.sofre_dano(dano)
    def tenta_captura(self):
        if self.player.inventario['selo de captura'] > 0:
            sucesso=random.choice([True,False])
            if sucesso:
                self.capturou = 'Seu selamento funcionou, você capturou o {0}'.format(self.A.nome)
                self.adversario.hp=self.adversario.monstro.hp
                self.player.captura(self.adversario)
                self.player.inventario['selo de captura']-=1
            else:
                self.capturou = 'Seu selamento falhou, a energia está livre'
                self.c+=1
        else:
            self.capturou = 'Você não tem mais selos de captura, a energia se discipou'
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
                        self.disponivel = 0
                        for d in self.player.party:
                            self.T=True
                            if d.hp > 0:
                                self.disponivel+=1
                        self.condicao = 'trocar'
                    if event.key == pg.K_SPACE:
                        self.forcegoback()
                if self.condicao == 'combate':
                    if event.key == pg.K_q: 
                        self.golpe = self.criaturaP.moves[0]
                        self.atacar()
                        self.condicao = 'atacando'
                    if event.key == pg.K_w:
                        if len(self.criaturaP.moves)>=2:
                            self.golpe = self.criaturaP.moves[1]
                            self.atacar()
                            self.condicao = 'atacando'
                        else:
                            pass
                    if event.key == pg.K_e:
                        if len(self.criaturaP.moves)>=3:
                            self.golpe = self.criaturaP.moves[2]
                            self.atacar()
                            self.condicao = 'atacando'
                        else:
                            pass
                    if event.key == pg.K_r:
                        if len(self.criaturaP.moves)>=4:
                            self.golpe = self.criaturaP.moves[3]
                            self.atacar()
                            self.condicao = 'atacando'
                        else:
                            pass
                    if event.key == pg.K_SPACE:
                        self.condicao = 'escolha'
                if self.condicao == 'atacando':
                    if event.key == pg.K_SPACE:
                        if self.c < 1:
                            self.c+=1
                        else:
                            self.c=0
                            if self.adversario.hp == 0:
                                self.condicao = 'ganhou'
                            else:
                                self.c=0
                                self.atacado()
                                self.condicao = 'atacado'
                if self.condicao == 'atacado':
                    if event.key == pg.K_SPACE:
                        if self.c <= 1:
                            self.c+=1
                        else:                                
                            self.c=0
                            if self.criaturaP.hp == 0:
                                self.condicao = 'perdeu'
                            else:
                                self.condicao = 'escolha'
                if self.condicao == 'falhou fugir':
                    if event.key == pg.K_SPACE: 
                        self.atacado()
                        self.condicao = 'atacado'
                if self.condicao == 'ganhou':
                    if event.key == pg.K_SPACE:
                        if self.c == 0:
                            self.c+=1
                        elif self.c == 1:
                            self.condicao = 'captura'
                            self.criaturaP.lvup(self,self.adversario.lv)
                            self.c=0
                if self.condicao == 'perdeu':
                    if event.key == pg.K_SPACE:
                        self.disponivel = 0
                        for d in self.player.party:
                            if d.hp > 0:
                                self.disponivel+=1
                        if self.disponivel>0:
                            self.condicao = 'trocar'
                        else:
                            self.forcegoback()
                if self.condicao == 'trocar':
                    if event.key == pg.K_SPACE:
                        if self.disponivel == 0:
                            self.game.morte
                            self.forcegoback
                        if self.T:
                            self.condicao = 'escolha' 
                    if event.key == pg.K_1:
                        if self.player.party[0].hp>0:
                            self.criaturaP=self.player.party[0]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_2:
                        if len(self.player.party)>=2 and self.player.party[1].hp>0:
                            self.criaturaP=self.player.party[1]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_3:
                        if len(self.player.party)>=3 and self.player.party[2].hp>0:
                            self.criaturaP=self.player.party[2]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_4:
                        if len(self.player.party)>=4 and self.player.party[3].hp>0:
                            self.criaturaP=self.player.party[3]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_5:
                        if len(self.player.party)>=5 and self.player.party[4].hp>0:
                            self.criaturaP=self.player.party[4]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_6:
                        if len(self.player.party)>=6 and self.player.party[5].hp>0:
                            self.criaturaP=self.player.party[5]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_7:
                        if len(self.player.party)>=7 and self.player.party[6].hp>0:
                            self.criaturaP=self.player.party[6]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                    if event.key == pg.K_8:
                        if len(self.player.party)>=8 and self.player.party[7].hp>0:
                            self.criaturaP=self.player.party[7]
                            if self.T:
                                self.atacado()
                                self.condicao='atacado'
                            else:
                                self.condicao = 'escolha'
                if self.condicao == 'captura':
                    if self.c==0:
                        if event.key == pg.K_s:
                            self.c+=1
                            self.tenta_captura()
    
                        if event.key == pg.K_n:
                            self.capturou = 'Você deixou a energia da craitura se dissipar'
                            self.c=2
                    if self.c==1:
                        if event.key == pg.K_SPACE:
                            self.c+=1
                    if self.c==2:
                        if event.key == pg.K_SPACE:
                            if self.capturou == 'Você deixou a energia da craitura se dissipar'   or 'Você não tem mais selos de captura, a energia se discipou':
                                self.forcegoback()
                            if self.capturou == 'Seu selamento falhou, a energia está livre':
                                self.capturou = 'Gostaria de tentar novamente'
                                self.c=0
                            if self.capturou == 'Seu selamento funcionou, você capturou o {0}'.format(self.A.nome):
                                if len (self.player.party) == self.player.partysize:
                                    self.c+=1
                                else:
                                    self.forcegoback()
                    if self.c == 3:
                        if event.key == pg.K_SPACE:
                            self.c+=1
                    if self.c == 4:
                        if event.key == pg.K_SPACE:
                            self.forcegoback()
                if self.condicao == 'item':
                    if event.key == pg.K_1:
                        if len(self.lista_itens)>=1:
                            self.criaturaP.cura(self.lista_itens[0].cura)
                            self.player.gasta_item(self.lista_itens[0])
                            if self.lista_itens[0] not in self.player.inventario:
                                del self.lista_itens[0]
                            self.condicao = 'escolha'
                    if event.key == pg.K_2:
                        if len(self.lista_itens)>=2:
                            self.criaturaP.cura(self.lista_itens[1].cura)
                            self.player.gasta_item(self.lista_itens[1])
                            if self.lista_itens[1] not in self.player.inventario:
                                del self.lista_itens[1]
                            self.condicao = 'escolha'
                    if event.key == pg.K_3:
                        if len(self.lista_itens)>=3:
                            self.criaturaP.cura(self.lista_itens[2].cura)
                            self.player.gasta_item(self.lista_itens[2])
                            if self.lista_itens[2] not in self.player.inventario:
                                del self.lista_itens[2]
                            self.condicao = 'escolha'
                    if event.key == pg.K_4:
                        if len(self.lista_itens)>=4:
                            self.criaturaP.cura(self.lista_itens[3].cura)
                            self.player.gasta_item(self.lista_itens[3])
                            if self.lista_itens[3] not in self.player.inventario:
                                del self.lista_itens[3]
                            self.condicao = 'escolha'
                    if event.key == pg.K_5:
                        if len(self.lista_itens)>=5:
                            self.criaturaP.cura(self.lista_itens[4].cura)
                            self.player.gasta_item(self.lista_itens[4])
                            if self.lista_itens[4] not in self.player.inventario:
                                del self.lista_itens[4]
                            self.condicao = 'escolha'
                    if event.key == pg.K_6:
                        if len(self.lista_itens)>=6:
                            self.criaturaP.cura(self.lista_itens[5].cura)
                            self.player.gasta_item(self.lista_itens[5])
                            if self.lista_itens[5] not in self.player.inventario:
                                del self.lista_itens[5]
                            self.condicao = 'escolha'
                    if event.key == pg.K_7:
                        if len(self.lista_itens)>=7:
                            self.criaturaP.cura(self.lista_itens[6].cura)
                            self.player.gasta_item(self.lista_itens[6])
                            if self.lista_itens[6] not in self.player.inventario:
                                del self.lista_itens[6]
                            self.condicao = 'escolha'
                    if event.key == pg.K_8:
                        if len(self.lista_itens)>=8:
                            self.criaturaP.cura(self.lista_itens[7].cura)
                            self.player.gasta_item(self.lista_itens[7])
                            if self.lista_itens[7] not in self.player.inventario:
                                del self.lista_itens[7]
                            self.condicao = 'escolha'
                    if event.key == pg.K_SPACE:
                        self.condicao = 'escolha'
                if self.condicao == 'subiu nivel':
                    if self.c == 0:
                        if event.key == pg.K_SPACE:
                            if self.criaturaP.lv in self.M.move_pool.values():
                                for m,nv in self.M.move_pool.items():
                                    if self.criaturaP.lv == nv:
                                        self.golpe = m
                                self.c += 1
                            else:
                                self.condicao = 'captura'
                    if self. c == 1:
                        if event.key == pg.K_s:
                            if len (self.criaturaP.moves)<4:
                                self.criaturaP.moves.append(self.golpe)
                                self.condicao = 'captura'
                            self.c+=1
                        if event.key == pg.K_n:
                            self.condicao = 'captura'
                    if self. c == 2:
                        if event.key == pg.K_SPACE:
                            self.c+=1
                    if self. c == 3:
                        if event.key == pg.K_q:
                            self.criaturaP.troca_golpe(0,self.golpe)
                            self.condicao = 'captura'
                        if event.key == pg.K_w:
                            self.criaturaP.troca_golpe(1,self.golpe)
                            self.condicao = 'captura'
                        if event.key == pg.K_e:
                            self.criaturaP.troca_golpe(2,self.golpe)
                            self.condicao = 'captura'
                        if event.key == pg.K_r:
                            self.criaturaP.troca_golpe(3,self.golpe)
                            self.condicao = 'captura'