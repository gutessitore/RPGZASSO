# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 14:18:08 2018

@author: gugat
"""
# RPGzao

import pygame

pygame.init()

#Determina a altura e a largura da janela principal
altura = 800
largura = 600

#Define o titulo da janela
gameDisplay = pygame.display.set_mode((altura, largura))
pygame.display.set_caption('Quest for the Swords')

#Define cores RGB
black = (0,0,0)
white = (255,255,255)

relogio = pygame.time.Clock()

#Determina a condição do loop principal do jogo
vivo = True

#carrega as imagens do jogo
boneco = pygame.image.load('boneco.png')
boneco_mask = pygame.image.load('boneco_mask.png').convert_alpha()
mapa = pygame.image.load('mapao.png')
mapaS = pygame.image.load('mapaSuperior.png')
fundo = pygame.image.load('fundo.png')

mapa_mask = pygame.image.load('map_mask.png').convert_alpha()
mascara_mapa = pygame.mask.from_surface(mapa_mask)
mapa_mask_centro = mapa_mask.get_rect()
x_mapa = (1280/2) - mapa_mask_centro.center[0]
y_mapa = (1280/2) - mapa_mask_centro.center[1]


mapa_saidaC = pygame.image.load('saidaDaCidade.png').convert_alpha()
saida_da_cidade = pygame.mask.from_surface(mapa_saidaC)


bonecoM = pygame.mask.from_surface(boneco_mask)

#Funções para colocar imagens na janela
def posicao_boneco(x,y):
    gameDisplay.blit(boneco, (x,y))
def posicao_boneco_mask(x,y):
    gameDisplay.blit(boneco_mask, (x,y))
def posicao_mapa(x,y):
    gameDisplay.blit(mapa, (x,y))
def posicao_mapa_mask(x,y):
    gameDisplay.blit(mapa_mask, (x,y))    
def posicao_mapaS(x,y):
    gameDisplay.blit(mapaS, (x,y))
def posicao_saida(x,y):
    gameDisplay.blit(mapa_saidaC, (x,y))    


#Posição inicial do boneco
x_b =  (altura * 0.45)
y_b = (largura * 0.45)

#posição inicial do mapa
x_m = -1511
y_m = -1684

#x_m_ é o eixo x do Mapa e x_m é o eixo x da mascara de colisão do mapa
x_m_ = x_m
y_m_ = y_m

#velocidades(e = esquerda, d = direita c = cima, b = baixo)
vxe = 0
vyc = 0
vxd = 0
vyb = 0

#inicia o loop da musica 
pygame.mixer.music.load('Overworld.ogg')
pygame.mixer.music.play(-1)

sair = 0

#Loop principal do jogo
while vivo:
    
    #resultado é a variavel que define se existe colisão entre o boneco e o mapa
    offset = (int(x_b - x_m), int(y_b - y_m))
    resultado = mascara_mapa.overlap(bonecoM, offset)
    
    #define se existe contado entre a mascara 'sair da cidade' e o boneco
    sair_da_cidade = saida_da_cidade.overlap(bonecoM, offset)
     
    #Atualiza a posição da mascara do mapa
    if x_m != x_m_:
        x_m = x_m_

    if y_m != y_m_:
        y_m = y_m_
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vivo = False
                  
        #Adiciona velocidade ao mapa
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:                    
                vxe = 2
                                                   
            if event.key == pygame.K_d: 
                vxd = 2
                                   
            if event.key == pygame.K_w:
                vyc = 2           
                    
            if event.key == pygame.K_s:
                vyb = 2
                
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_a:
                vxe = 0
                                      
            if event.key == pygame.K_d:
                vxd = 0                                                                       
                    
            if event.key == pygame.K_w:
                vyc = 0
                       
            if event.key == pygame.K_s:
                vyb = 0
              
    #move a mascara do mapa e verifica se existe colisão, para depois mover o mapa           
    x_m -= vxd

    if not resultado:
        x_m_ -= vxd
        
    x_m += vxe
    
    if not resultado:
        x_m_ += vxe
        
    y_m += vyc
    
    if not resultado:
        y_m_ += vyc
        
    y_m -= vyb
    
    if not resultado:
        y_m_ -= vyb
   
#    print(resultado)     
#    print(x_b, y_b, 'boneco')
#    print(x_m_, y_m_, 'mapa')
    
    #Coloca as imagens na janela
    gameDisplay.fill(white)
    
    posicao_saida(x_m, y_m)
    posicao_boneco_mask(x_b, y_b)
    posicao_mapa(x_m_, y_m_)
    posicao_boneco(x_b, y_b)
    posicao_mapaS(x_m_, y_m_)
  
    if sair_da_cidade:
        sair += 1
        
    if sair == 1:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('boraBatalha.ogg')
        pygame.mixer.music.play(-1)

    pygame.display.update()
    relogio.tick(1000)
    
pygame.quit()
quit()