import pygame as pg
import settings

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rot = 90
        self.inventario={}
        self.party=[]
        self.capturas=[]
        self.partysize=4
        
    def ganha_item(self, item):
        if item not in self.inventario:
            self.inventario[item]=1
        else:
            self.inventario[item]+=1
    
    def captura(self, criatura):
        self.capturas.append(criatura)
        if len(self.party)<=self.partysize:
            self.party.append(criatura)
            
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * settings.TILESIZE
        self.rect.y = self.y * settings.TILESIZE

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
class Bau(pg.sprite.Sprite):
    def __init__(self, game, x, y, item):
        self.groups = game.all_sprites, game.baus, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.aberto = False
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        if self.aberto == False:
            self.image.fill(settings.AMARELO)
        else:
            self.image.fill(settings.AMARELO_ESC)
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
            self.image.fill(settings.AMARELO)
        else:
            self.image.fill(settings.AMARELO_ESC)
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
    def sofre_dano(self,dano):
        self.monstro.hp-=dano
class Golpes():
    def __init__(self,nome, tipo, dano):
        self.nome=nome
        self.tipo = tipo
        self.dano = dano
class Tipo():
    def __init__(self, resistencia, fraqueza):
        self.resistencia=resistencia
        self.fraquesa=fraqueza
        
        
