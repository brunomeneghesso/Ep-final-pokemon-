import pygame as pg
import sys
from os import path
import settings
import sprites
import tilemap
import combate

lista_baus=[[18,5,"batata frita"], [18,1,"xicara de cafe"], [6,6,"orelha do papai noel"]] 
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption(settings.TITULO)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(200,100)
        self.load_data()
        self.abrindo = False

    def coloca_monstros(self):
        self.superEf=sprites.Tipo([],[])
        self.poucoEf=sprites.Tipo([],[])
        self.neutro=sprites.Tipo([],[])
        self.testeTip = sprites.Tipo([self.poucoEf][self.superEf])
        
        self.testeMov=sprites.Golpes('golpe neutro',self.neutro, 10)
        self.testeSuper=sprites.Golpes('super efetivo', self.superEf, 10)
        self.testePouco=sprites.Golpes('pouco efetivo', self.poucoEf, 10)
        self.testeSTB=sprites.Golpes('STB', self.testeTip, 10)
        
        self.monstro_teste = sprites.Monstro(self, self.testeTip, 'teste1', 1, 10, 50, [self.testeMov, self.testeSuper,self.testePouco,self.testeSTB], 'imgteste.png', [1,1,1], 1)

        self.player.captura(sprites.Criatura([self.testeMov, self.testeSuper,self.testePouco,self.testeSTB], 1, 0, self.monstro_teste))
                
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Textures')
        self.map = tilemap.Map(path.join(game_folder, 'mapa_teste.txt'))
        self.player_img = pg.image.load(path.join(img_folder, "char.png")).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, "wall.png")).convert_alpha()
        #self.bau_a_img = pg.image.load(path.join(img_folder, "bau aberto.png")).convert()
        #self.bau_f_img = pg.image.load(path.join(img_folder, "bau fechado.png")).convert()
        self.font=settings.fonte
        self.coloca_monstros

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.baus = pg.sprite.Group()
        self.player = pg.sprite.Group()
        for l in lista_baus:
            sprites.Bau(self, l[0], l[1], l[2])
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    sprites.Wall(self, col, row)
                if tile == 'P':
                    self.player = sprites.Player(self, col, row)
        self.camera = tilemap.Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.CINZA_CLA, (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.CINZA_CLA, (0, y), (settings.WIDTH, y))
    def combate(self):
        c = combate.Combate_central(self.screen, self.all_sprites, self.camera, self.player)
        c.run()
            
    def draw(self):
        self.screen.fill(settings.BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.abrindo == True:
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/5, settings.HEIGHT*7/8, settings.WIDTH*3/5, settings.HEIGHT/8])
            text_surface = settings.fonte.render("Você ganhou 1 {0}!".format(self.Ba.conteudo), True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *9 / 10)
            self.screen.blit(text_surface, text_rect)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()
    def events(self):
        if not self.abrindo:
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
                    if event.key == pg.K_c:
                        self.save=[self.all_sprites, self.camera]
                        self.combate()
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
                                    self.Ba=B
                                    self.abrindo = True
                                    self.first = True
        elif self.abrindo == True: 
            if self.first:
                self.Ba.abre()
                self.player.ganha_item(self.Ba.conteudo)
                self.first = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_SPACE:
                        self.abrindo = False

        
        
        
        
        

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
    

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
g.show_go_screen()