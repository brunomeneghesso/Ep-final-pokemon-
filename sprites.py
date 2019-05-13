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
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.image.fill(settings.VERDE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
class Bau(pg.sprite.Sprite):
    def __init__(self, game, x, y, item, op):
        self.groups = game.all_sprites, game.baus, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.aberto = op
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
class Monstro(pg.sprite.Sprite):
    def __init__(self, game, tipo, move_pool, imagem, crescimento, explv):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.tipo = tipo
        self.move_pool = move_pool
        self.image = imagem
        self.crescismento = crescimento
        self.explv = explv
class criatura(Monstro):
    def __init__(self, moves, lv, exp):
        self.moves = moves
        self.lv = lv
        self.exp = exp
class Golpes():
    def __init__(self, game, tipo, dano, bonus):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.tipo = tipo
        self.dano = dano
        self.bonus = bonus