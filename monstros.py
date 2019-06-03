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
    game.agua1 = sprites.Golpes('Rajada de água', game.agua, 10,10)
    game.agua2 = sprites.Golpes('Hidro-lâmina', game.agua, 15,20)
    game.planta1 = sprites.Golpes('Chicote de vinha', game.planta, 10,10)
    game.planta2 = sprites.Golpes('Raiz penetrante', game.planta, 15,20)
    
    game.monstro_teste = sprites.Monstro('monstro teste', [game.testeTip], 1, 1, 200,100, [game.testeMov, game.testeSuper,game.testePouco,game.testeSTB], pg.image.load(path.join(img_folder, "imgteste.png")).convert(), [1,1,1,1], 1)