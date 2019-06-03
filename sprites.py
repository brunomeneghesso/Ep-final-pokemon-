import pygame as pg
import settings
import random

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = 90
        self.image = game.player_img_up
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.inventario={'selo de captura':10}
        self.party=[]
        self.capturas=[]
        self.partysize=8
        
    def ganha_item(self, item):
        if item not in self.inventario:
            self.inventario[item]=1
        else:
            self.inventario[item]+=1
    
    def captura(self, criatura):
        if len(self.party)<=self.partysize:
            self.party.append(criatura)
        else:
            self.capturas.append(criatura)
            
    def move(self, dx=0, dy=0, rodar=90):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
        self.rot=rodar
        if self.testa_combate(dx, dy):
            self.game.combate() 
    
    def testa_combate(self, dx=0, dy=0):
        for m in self.game.mato:
            if m.x == self.x + dx and m.y == self.y + dy:
                n = random.randint(0,10)
                if n == 7:
                    return True
        return False
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * settings.TILESIZE
        self.rect.y = self.y * settings.TILESIZE
        if self.rot == 90:
            self.image = self.game.player_img_up
        if self.rot == 0:
            self.image = self.game.player_img_right
        if self.rot == 180:
            self.image = self.game.player_img_left
        if self.rot == 270:
            self.image = self.game.player_img_down

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
        
class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.ground_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
        
class Bau(pg.sprite.Sprite):
    def __init__(self, game, x, y, item):
        self.groups = game.all_sprites, game.baus, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.aberto = False
        if self.aberto == False:
            self.image=self.game.bau_f_img
        else:
            self.image=self.game.bau_a_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
        self.conteudo = item
    def abre (self):
        self.aberto = True
    def update (self):
        if self.aberto == False:
            self.image=self.game.bau_f_img
        else:
            self.image=self.game.bau_a_img
class Monstro(pg.sprite.Sprite):
    def __init__(self, nome, tipo, ataque, defesa, vida, move_pool, imagem, crescimento, explv):
        self.nome = nome
        self.image = imagem
        self.rect = self.image.get_rect()
        self.tipo = tipo
        self.move_pool = move_pool
        self.crescimento = crescimento
        self.explv = explv
        self.hp = vida
        self.atk = ataque
        self.df = defesa
class Criatura(Monstro):
    def __init__(self, moves, lv, exp, monstro):
        self.moves = moves
        self.lv = lv
        self.exp = exp
        self.monstro=monstro
        self.hp=self.monstro.hp
        
    def sofre_dano(self,dano):
        self.hp-=dano
        if self.hp < 0:
            self.hp = 0
    def lvup(self,lva):
        self.exp+=10*self.lv/lva
        if self.exp>self.monstro.explv*self.lv:
            self.exp-=self.monstro.explv*self.lv
            self.lv+=1
class Golpes():
    def __init__(self,nome, tipo, dano):
        self.nome=nome
        self.tipo = tipo
        self.dano = dano
class Tipo():
    def __init__(self, resistencia, fraqueza):
        self.resistencia=resistencia
        self.fraquesa=fraqueza
        
class Mato(pg.sprite.Sprite):
    def __init__(self, game, x, y, monstros, lvmin, lvmax):
        self.groups = game.mato
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grass_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
        self.monstros = monstros
        self.lvmin = lvmin
        self.lvmax = lvmax
        

class Grass_skin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grass_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
    
class Background_ini(pg.sprite.Sprite):
    def __init__(self, game, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initialize
        self.image = game.inicio
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
class Background_end(pg.sprite.Sprite):
    def __init__(self, game, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initialize
        self.image = game.fim
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
class Background_combat(pg.sprite.Sprite):
    def __init__(self, game, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initialize
        self.image = game.combat_back
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
