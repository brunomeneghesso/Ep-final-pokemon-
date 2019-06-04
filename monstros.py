from os import path
import sprites
import pygame as pg
def coloca_monstros(game):
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'Textures')
    #testes
    game.superEf=sprites.Tipo("super ef",[],[])
    game.poucoEf=sprites.Tipo("pouco ef",[],[])
    game.neutro=sprites.Tipo("neutro",[],[])
    game.testeTip = sprites.Tipo('teste',["pouco ef"],["super ef"])
    
    #tipos do jogo
    game.neutro = sprites.Tipo('neutro',[],[])
    game.fogo = sprites.Tipo("fogo",["planta"],["água"])
    game.agua = sprites.Tipo("água",["fogo"],["planta"])
    game.planta = sprites.Tipo("planta",["água"],["fogo"])

    #testes
    game.testeMov=sprites.Golpes('golpe neutro',game.neutro, 10,10)
    game.testeSuper=sprites.Golpes('super efetivo', game.superEf, 10,20)
    game.testePouco=sprites.Golpes('pouco efetivo', game.poucoEf, 10,5)
    game.testeSTB=sprites.Golpes('STB', game.testeTip, 10,15)
    
    game.fogo1 = sprites.Golpes('Garras de fogo', game.fogo, 10,10)
    game.fogo2 = sprites.Golpes('Chama ardente', game.fogo, 15,20)
    game.fogo3 = sprites.Golpes('Fornalha infernal', game.fogo, 50, 75)
    game.agua1 = sprites.Golpes('Rajada de água', game.agua, 10,10)
    game.agua2 = sprites.Golpes('Hidro-lâmina', game.agua, 15,20)
    game.agua3 = sprites.Golpes('Tormenta', game.agua, 50, 75)
    game.planta1 = sprites.Golpes('Chicote de vinha', game.planta, 10,10)
    game.planta2 = sprites.Golpes('Raiz penetrante', game.planta, 15,20)
    game.planta3 = sprites.Golpes('Espinhos crescentes', game.planta, 50,75)
    game.neutro1 = sprites.Golpes('Derrubada', game.neutro, 15, 5)
    game.neutro2 = sprites.Golpes('Arranhar', game.neutro, 20, 15)
    game.neutro3 = sprites.Golpes('Soco cruzado', game.neutro, 30, 25)

    
    
    game.monstro_teste = sprites.Monstro('monstro teste', [game.testeTip], 1, 1, 200,100, {game.testeMov:0, game.testeSuper:0,game.testePouco:0,game.testeSTB:0}, pg.image.load(path.join(img_folder, "imgteste.png")).convert(),pg.image.load(path.join(img_folder, "imgteste2.png")).convert(), [1,1,1,1], 1)
    game.inicial_fogo = sprites.Monstro('Agni', [game.fogo], 3, 8, 100, 100, {game.fogo1:0,game.neutro1:0, game.neutro2:7, game.fogo2:15, game.neutro3:30, game.fogo3:45}, pg.image.load(path.join(img_folder, "fogo.png")).convert(),pg.image.load(path.join(img_folder, "fogo2.png")).convert(), [3,5,10,10],20)
    game.inicial_agua = sprites.Monstro('Nautica', [game.agua], 2, 12, 120, 100, {game.agua1:0,game.neutro1:0, game.neutro2:7, game.agua2:15, game.neutro3:30, game.agua3:45}, pg.image.load(path.join(img_folder, "agua.png")).convert(),pg.image.load(path.join(img_folder, "agua2.png")).convert(), [2,7,12,8],20)
    game.inicial_planta = sprites.Monstro('Grover', [game.fogo], 1, 16, 150, 100, {game.planta1:0,game.neutro1:0, game.neutro2:7, game.planta2:15, game.neutro3:30, game.planta3:45}, pg.image.load(path.join(img_folder, "planta.png")).convert(),pg.image.load(path.join(img_folder, "planta2.png")).convert(), [1,10,15,15],20)