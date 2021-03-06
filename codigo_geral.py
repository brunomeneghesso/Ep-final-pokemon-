import pygame as pg
import sys
import time
from os import path
import settings
import sprites
import tilemap
import combate
import monstros
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption(settings.TITULO)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(200,100)
        self.load_data()
        self.abrindo = False
        self.curando = False
        self.troca = False
        self.c=0
    def coloca_itens(self):
        self.item1 = sprites.item('poção P',20)
        self.item2 = sprites.item('poção M',50)
        self.item3 = sprites.item('poção G',200)

    def coloca_monstros(self):
        monstros.coloca_monstros(self) 
    def load_data(self):
        self.game_over = False
        self.start_on = True
        self.start_on2 = True
        self.end_on = True
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Textures')
        ground_folder = path.join(img_folder, "ground")
        char_folder = path.join(img_folder, "char")
        wall_folder = path.join(img_folder, "wall")
        #map
        self.map = tilemap.Map(path.join(game_folder, 'mapa mato.txt'))
        self.map2 = tilemap.Map(path.join(game_folder, 'mapa castelo.txt'))
        self.player_img_up = pg.image.load(path.join(char_folder, "char_up.png")).convert_alpha()
        self.player_img_down = pg.image.load(path.join(char_folder, "char_down.png")).convert_alpha()
        self.player_img_left = pg.image.load(path.join(char_folder, "char_left.png")).convert_alpha()
        self.player_img_right = pg.image.load(path.join(char_folder, "char_right.png")).convert_alpha()
        self.tilezito = pg.image.load(path.join(ground_folder, "tilezito.png")).convert_alpha()
        self.wall_img = pg.image.load(path.join(wall_folder, "wall.png")).convert_alpha()
        self.tree_wall_img = pg.image.load(path.join(wall_folder, "tree.png")).convert_alpha()
        self.stone_ground_img = pg.image.load(path.join(ground_folder, "stone_brick.png")).convert_alpha()
        self.dirt_ground_img = pg.image.load(path.join(ground_folder, "ground2.png")).convert_alpha()
        self.lake = pg.image.load(path.join(img_folder, "lake.png")).convert_alpha()
        self.stone_grass_img = pg.image.load(path.join(ground_folder, "mossy_stone_brick.png")).convert_alpha()
        self.dirt_grass_img = pg.image.load(path.join(ground_folder, "grass2.png")).convert_alpha()
        self.tall_grass_img = pg.image.load(path.join(ground_folder, "grass3.png")).convert_alpha()
        self.bau_a_img = pg.image.load(path.join(img_folder, "bau_aberto.png")).convert()
        self.bau_f_img = pg.image.load(path.join(img_folder, "bau_fechado.png")).convert()
        self.inicio = pg.image.load(path.join(img_folder, "start_screen.png")).convert()
        self.fim = pg.image.load(path.join(img_folder, "end_screen.png")).convert()
        self.combat_back = pg.image.load(path.join(img_folder, "combat_background.png")).convert()
        self.escolha = pg.image.load(path.join(img_folder, "escolha.png")).convert()
        self.cura_img = pg.image.load(path.join(img_folder, "cura.png")).convert()
        self.pc_img = pg.image.load(path.join(img_folder, "pc.png")).convert()
        self.font=settings.fonte
        self.font40=settings.fonte_combate
        self.font20=settings.fonte_legenda
        self.coloca_monstros()
        self.coloca_itens()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.baus = pg.sprite.Group()
        self.mato = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.cura = pg.sprite.Group()
        self.screen.fill(settings.VERDE)
        self.pc = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    sprites.Grass_ground(self, col, row)
                if tile == '1':
                    sprites.Wall_tree(self, col, row)
                if tile == "c":
                    sprites.Ground_stone_wall(self, col, row)
                if tile == "=" or tile == 'P':
                    sprites.Ground_dirt(self, col, row)
                if tile == "+":
                    sprites.Tilezito(self, col, row)
                if tile == "o":
                    sprites.Lake(self, col, row)
                if tile == "w":
                    sprites.Mato(self,col,row,[self.inicial_fogo, self.inicial_agua, self.inicial_planta],3,6)
                    sprites.Grass_real(self, col, row)
                if tile == "W":
                    sprites.Mato(self,col,row,[self.inicial_fogo, self.inicial_agua, self.inicial_planta],6,12)
                    sprites.Grass_real(self, col, row)
                if tile == "m":
                    sprites.Mato(self,col,row,[self.inicial_fogo, self.inicial_agua, self.inicial_planta],10,18)
                    sprites.Grass_real(self, col, row)
                if tile == "M":
                    sprites.Mato(self,col,row,[self.inicial_fogo, self.inicial_agua, self.inicial_planta],16,25)
                    sprites.Grass_real(self, col, row)
                if tile == "j":
                    sprites.Mato(self,col,row,[self.inicial_fogo, self.inicial_agua, self.inicial_planta],16,25)
                    sprites.Grass_stone(self, col, row)
                if tile == "U":
                    sprites.Cura(self,col,row)
                if tile == "C":
                    sprites.PC(self,col,row)
                if tile == "p":
                    sprites.Bau(self, col, row, self.item1)
                if tile == "x":
                    sprites.Bau(self,col,row,self.item2)
                if tile == "g":
                    sprites.Bau(self,col,row,self.item3)


        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = sprites.Player(self, col, row)
                    if self.inicial == 'planta':
                        self.player.captura(sprites.Criatura([self.planta1,self.neutro1], 5, 0, self.inicial_planta))
                    if self.inicial == 'agua':
                        self.player.captura(sprites.Criatura([self.agua1,self.neutro1], 5, 0, self.inicial_agua))
                    if self.inicial == 'fogo':
                        self.player.captura(sprites.Criatura([self.fogo1,self.neutro1], 5, 0, self.inicial_fogo))

        self.camera = tilemap.Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS) / 1000.0
            self.check_tp()
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
        mato_teste = sprites.Mato(self,0,0,[self.inicial_fogo, self.inicial_agua, self.inicial_planta],3,6)
        c = combate.Combate_central(self, self.screen, self.all_sprites, self.camera, self.player, mato_teste)
        c.run()
            
    def draw(self):
        self.screen.fill(settings.BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.abrindo == True:
            pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/5, settings.HEIGHT*7/8, settings.WIDTH*3/5, settings.HEIGHT/8])
            text_surface = self.font.render("Você ganhou 1 {0}!".format(self.Ba.conteudo.nome), True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *9 / 10)
            self.screen.blit(text_surface, text_rect)
        if self.curando == True:
            pg.draw.rect(self.screen, settings.MARROM_ESC,[0, settings.HEIGHT*7/8, settings.WIDTH, settings.HEIGHT/8])
            if self.c == 0:
                text_surface = self.font.render("Você colocou suas criaturas na fonte de vida", True, settings.BRANCO)
            else:
                text_surface = self.font.render("{0} e suas outras criaturas estão curadas!".format(self.player.party[0].monstro.nome), True, settings.BRANCO)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.WIDTH / 2,  settings.HEIGHT *9 / 10)
            self.screen.blit(text_surface, text_rect)
        if self.troca == True:
            if self.c == 0:
                pg.draw.rect(self.screen, settings.BEJE,[0, settings.HEIGHT*2/3, settings.WIDTH, settings.HEIGHT/3])
                   
                text_surface = self.font.render("Substitua seus magimons", True, settings.PRETO)
                text_rect = text_surface.get_rect()
                text_rect.center = (settings.WIDTH / 2,  settings.HEIGHT *9 / 12)
                self.screen.blit(text_surface, text_rect)
                
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/10-16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
                pg.draw.rect(self.screen, settings.PRETO,[settings.WIDTH/2+16, settings.HEIGHT*2/3+settings.HEIGHT/6+16, settings.WIDTH*2/5, settings.HEIGHT/3*2/5])
                
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/10-12, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
                pg.draw.rect(self.screen, settings.MARROM_ESC,[settings.WIDTH/2+20, settings.HEIGHT*2/3+settings.HEIGHT/6+20, settings.WIDTH*2/5-8, settings.HEIGHT/3*2/5-8])
            
                text_surface = self.font20.render("Q", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/10-2, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
            
                text_surface = self.font.render("De em uso para morelo", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH*3/10-4, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
                    
                text_surface = self.font20.render("W", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+30, settings.HEIGHT*2/3+settings.HEIGHT/6+24)
                self.screen.blit(text_surface, text_rect)
                    
                text_surface = self.font.render("De morelo para em uso", True, settings.BRANCO)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (settings.WIDTH/2+12+settings.WIDTH/5, settings.HEIGHT*2/3+settings.HEIGHT/6+40)
                self.screen.blit(text_surface, text_rect)
               
            if self.c==1:
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
                for m in self.player.party:
                    text_surface = self.font20.render("{0}".format(X+1), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0]-(settings.WIDTH/5-20),pos[X][1]-((settings.HEIGHT-160)/8-24))
                    self.screen.blit(text_surface, text_rect)
                    text_surface = self.font40.render("{0}".format(m.monstro.nome), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0],pos[X][1])
                    self.screen.blit(text_surface, text_rect)
                    X+=1
            if self.c==2:
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
                for m in self.player.capturas:
                    text_surface = self.font20.render("{0}".format(X+1), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0]-(settings.WIDTH/5-20),pos[X][1]-((settings.HEIGHT-160)/8-24))
                    self.screen.blit(text_surface, text_rect)
                    text_surface = self.font40.render("{0}".format(m.monstro.nome), True, settings.BRANCO)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (pos[X][0],pos[X][1])
                    self.screen.blit(text_surface, text_rect)
                    X+=1
        pg.display.flip()

    def check_tp(self):
        if self.player.x == 61:
            if self.player.y == 40:
                self.tp()
                self.update()
        if self.player.x == 60:
            if self.player.y == 40:
                self.tp()
                self.update()
        if self.player.x == 59:
            if self.player.y == 40:
                self.tp()
                self.update()
        if self.player.x == 62:
            if self.player.y == 40:
                self.tp()
                self.update()
        if self.player.x == 51:
            if self.player.y == 25:
                self.tp2()
                self.update()
        if self.player.x == 49:
            if self.player.y == 25:
                self.tp2()
                self.update()
        if self.player.x == 50:
            if self.player.y == 25:
                self.tp2()
                self.update()

    def tp(self):
        self.player.tp( 50, 24)
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        self.draw()
        
    def tp2(self):
        self.player.tp( 60, 41)
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        self.draw()

    def events(self):
        if not self.abrindo and not self.curando and not self.troca:
        # catch all events here
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_LEFT:
                        self.player.move(dx=-1,rodar=180)
                    if event.key == pg.K_g:
                        self.morte()
                    if event.key == pg.K_RIGHT:
                        self.player.move(dx=1,rodar=0)
                    if event.key == pg.K_UP:
                        self.player.move(dy=-1,rodar=90)
                    if event.key == pg.K_DOWN:
                        self.player.move(dy=1,rodar=270)
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
                        for C in self.cura:
                            if C.x == ver[0] and C.y == ver[1]:
                                self.curando = True
                                self.first = True
                                self.c=0
                        for p in self.pc:
                            if p.x == ver[0] and p.y == ver[1]:
                                self.troca = True
                                self.c=0
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
        elif self.curando == True: 
            if self.first:
                for m in self.player.party:
                    m.cura(m.hpmax)
                    m.mana = m.manamax
                self.first = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_SPACE:
                        if self.c==0:
                            self.c+=1
                        else:
                            self.curando = False

        elif self.troca == True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if self.c == 0:
                        if event.key == pg.K_q:
                            if len (self.player.party)>=2:
                                self.c += 1
                        if event.key == pg.K_w:
                            if len (self.player.capturas)>=1:
                                self.c+=2
                        if event.key == pg.K_SPACE:
                            self.troca = False
    
                    if self.c == 1:
                        if event.key == pg.K_SPACE:
                            self.c = 0
                        if event.key == pg.K_1:
                            self.player.capturas.append(self.player.party[0])
                            del(self.player.party[0])
                            self.c=0
                        if event.key == pg.K_2:
                            self.player.capturas.append(self.player.party[1])
                            del(self.player.party[1])
                            self.c=0
                            if event.key == pg.K_3:
                                if len (self.player.party)>=3:
                                    self.player.capturas.append(self.player.party[2])
                                    del(self.player.party[2])
                                    self.c=0
                            if event.key == pg.K_4:
                                if len (self.player.party)>=4:
                                    self.player.capturas.append(self.player.party[2])
                                    del(self.player.party[2])
                                    self.c=0
                    if self.c == 2:
                        if event.key == pg.K_SPACE:
                            self.c = 0
                        if len(self.player.party)<self.player.partysize:
                            if len(self.player.capturas)>=1:
                                if event.key == pg.K_1:
                                    self.player.party.append(self.player.capturas[0])
                                    del self.player.capturas[0]
                            if len(self.player.capturas)>=2:
                                if event.key == pg.K_2:
                                    self.player.party.append(self.player.capturas[1])
                                    del self.player.capturas[1]
                            if len(self.player.capturas)>=3:
                                if event.key == pg.K_3:
                                    self.player.party.append(self.player.capturas[2])
                                    del self.player.capturas[2]
                            if len(self.player.capturas)>=4:
                                if event.key == pg.K_4:
                                    self.player.party.append(self.player.capturas[3])
                                    del self.player.capturas[3]
                            if len(self.player.capturas)>=5:
                                if event.key == pg.K_5:
                                    self.player.party.append(self.player.capturas[4])
                                    del self.player.capturas[4]
                            if len(self.player.capturas)>=6:
                                if event.key == pg.K_6:
                                    self.player.party.append(self.player.capturas[5])
                                    del self.player.capturas[5]
                            if len(self.player.capturas)>=7:
                                if event.key == pg.K_7:
                                    self.player.party.append(self.player.capturas[6])
                                    del self.player.capturas[6]
                            if len(self.player.capturas)>=8:
                                if event.key == pg.K_8:
                                    self.player.party.append(self.player.capturas[7])
                                    del self.player.capturas[7]
    def morte(self):
        self.playing = False
        self.game_over = True
        
    def show_start_screen(self):
        background_init = sprites.Background_ini (self, [0,0])
        background_init2 = sprites.Background_ini2 (self, [0,0])
        while self.start_on:
            time.sleep(0.2)
            self.screen.blit(background_init.image, background_init.rect)
            self.screen.blit(self.tree_wall_img,(10,10))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_SPACE:
                        self.start_on = False
        while self.start_on2:
            time.sleep(0.2)
            self.screen.blit(background_init2.image, background_init2.rect)
            self.screen.blit(self.tree_wall_img,(10,10))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_q:
                        self.inicial = 'planta'
                        self.start_on2 = False
                    if event.key == pg.K_w:
                        self.inicial = 'fogo'
                        self.start_on2 = False
                    if event.key == pg.K_e:
                        self.inicial = 'agua'
                        self.start_on2 = False
         

    def show_go_screen(self):
        background_end = sprites.Background_end (self, [0,0])
        while self.end_on:
            time.sleep(0.2)
            self.screen.blit(background_end.image, background_end.rect)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_SPACE:
                        self.end_on = False
    

# create the game object
g = Game()
comback = g.combat_back
g.show_start_screen()
while not g.game_over:
    g.new()
    g.run()
g.show_go_screen()
pg.quit()