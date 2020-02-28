# Código fonte
'''
Estrutura do código baseado no tutorial do canal KidsCanCode:
https://www.youtube.com/playlist?list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i

Alterações:
criação de um sistema de mana para ultilização dos ataques basicos, que evolui com os niveis.
recuperacao de vida com a barra de espiritosS4
sistema de niveis de acordo com a quantidade de monstros mortos e seu tipo que evolui atributos do personagem principal
mecanica do personagem principal que atira em direção ao mouse 
monstros que evitam o personagem e atiram em sua direção
diferentes tipos de monstros com diferentes atributos, incluindo um 'Boss'
mapa desenhado no Tiled com a sprite sheet 'Megacity' : https://opengameart.org/content/mage-city-arcanos
sprite sheet dos monstros e personagems comprada no GameDev Market
alterações feitas nos sprites no GIMP
musicas utilizadas do site opengameart : https://opengameart.org/content/generic-8-bit-jrpg-soundtrack
fontes utilizada s8bitlim e 8bitlimo
feito por Gustavo Schlieper , Pedro Fontes & Gabriel Chinelato

'''
import pygame as pg
import sys
from os import path
from config import *
from sprites import *
from Mapa_Camera import *

# HUD
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = DARKRED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_mana(surf, x, y, pct):
    if pct < 0:
    	pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x , y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x , y, fill, BAR_HEIGHT)
    col = LIGHTBLUE
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_spirit(surf, x, y, pct):
    if pct < 0:
    	pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x , y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x , y, fill, BAR_HEIGHT)
    col = BRIGHTYELLOW
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_xp(surf, x, y, pct):
    BAR_LENGTH = 500
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = DARKGREEN
    pg.draw.Rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'imagens')
        map_folder = path.join(game_folder, 'map')
        self.title_font = path.join(img_folder, '8bitlim.ttf')
        self.map = TiledMap(path.join(map_folder, 'mapao.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, BONECO)).convert_alpha()
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET_1))
        self.magia_img = pg.image.load(path.join(img_folder, MAGIA_IMG)).convert_alpha()
        self.magia_f_img = pg.image.load(path.join(img_folder, MAGIA_F)).convert_alpha()
        self.magia_bolada_img = pg.image.load(path.join(img_folder, MAGIA_BOLADA)).convert_alpha()
        self.magia_b = pg.image.load(path.join(img_folder, MAGIA_B)).convert_alpha()
        self.spritesheet_boar = Spritesheet(path.join(img_folder, MONSTRO_IMG))
        self.spritesheet_element = Spritesheet(path.join(img_folder, ELEMENT_IMG))
        self.spritesheet_boss= Spritesheet(path.join(img_folder, BOSS_IMG))
        self.tela_df = pg.image.load(path.join(img_folder, TELA_INICIAL)).convert_alpha()
        self.tela_in = pg.image.load(path.join(img_folder, TELA_IN)).convert_alpha()
        self.tela_ini = pg.image.load(path.join(img_folder, TELA_INI)).convert_alpha()
        self.tela_go = pg.image.load(path.join(img_folder, TELA_OVER)).convert_alpha()
        self.tela_fi = pg.image.load(path.join(img_folder, TELA_FINAL)).convert_alpha()
        self.tela_mt = pg.image.load(path.join(img_folder, MAD_TITAN)).convert_alpha()
        self.dim = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim.fill((0, 0, 0, 150))
        self.musica_inicial = pg.mixer.music.load(path.join(path.join(game_folder, 'music'), MUSICA_INICIAL))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.magias_p = pg.sprite.Group()
        self.magias_m = pg.sprite.Group()
        self.magias_a = pg.sprite.Group()
        self.magias_b = pg.sprite.Group()
        self.atks = pg.sprite.Group()
        self.vida = pg.sprite.Group()


        for tile_object in self.map.tmxdata.objects:
        	if tile_object.name == 'player spawn':
        		self.player = Player(self, tile_object.x, tile_object.y)

        	if tile_object.name == 'mob spawn':
        		Monstro(self, tile_object.x, tile_object.y)

        	if tile_object.name == 'mob_f spawn':
        		Monstro_F(self, tile_object.x, tile_object.y)

        	if tile_object.name == 'mob_a spawn':
        		Monstro_A(self, tile_object.x, tile_object.y)

        	if tile_object.name == 'Boss spawn':
        		Boss(self, tile_object.x, tile_object.y)

        	if tile_object.name == 'parede':
        		Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        	if tile_object.name == 'vida':
        		Vida(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)
        self.ver = False
        self.pause = False

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.pause:
            	self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        hits_vida = pg.sprite.spritecollide(self.player, self.vida, False, collide_hit_rect)
        hits_m = pg.sprite.groupcollide(self.mobs, self.magias_p, False, True)
        hits_mm = pg.sprite.groupcollide(self.mobs, self.magias_m, False, True)
        hits_a = pg.sprite.spritecollide(self.player, self.magias_a, True, collide_hit_rect)
        hits_b = pg.sprite.groupcollide(self.mobs, self.magias_b, False, True)

        for hit in hits_vida:
        	if self.player.health < self.player.vida:
        		self.player.health += 5
        		if self.player.health > self.player.vida:
        			self.player.health = self.player.vida
        	if self.player.spirit < SPIRIT:
        		self.player.spirit += 1
        		if self.player.spirit > SPIRIT:
        			self.player.spirit = SPIRIT

        	#magik DMG
        for hit in hits_m:
        	dano_p = ATK_DMG * ((self.player.lvl / 10) + 1) + random.randrange(-5, 5)
        	hit.health -= dano_p

        for hit in hits_b:
        	dano_p = 220 * ((self.player.lvl / 10) + 1) + random.randrange(1, 50)
        	hit.health -= dano_p

        for hit in hits_mm:
        	dano_p = (ATK_DMG + 40) * ((self.player.lvl / 10) + 1) + random.randrange(-5, 5)
        	hit.health -= dano_p
         	# mob DMG
        for hit in hits:
        	if hit.type == 1:
        		dano = DANO_MONSTRO + random.randrange(-15,15)
        		self.player.health -= dano
        		hit.vel = vec(0, 0)
	        	if self.player.health <= 0:
	        		self.playing = False
        	if hit.type == 2:
        		self.player.health -= DANO_MONSTRO_F + random.randrange(-5, 10)
        		hit.vel = vec(0, 0)
	        	if self.player.health <= 0:
		       		self.playing = False

        for hit in hits_a:
        	self.player.health -= DANO_MONSTRO_A + random.randrange(-20, 20)
        	hit.vel = vec(0, 0)
        	if self.player.health <= 0:
        		self.playing = False

        if hits:
            self.player.pos += vec(MONTRO_PUSH, 0). rotate(-hits[0].rot)

        if len(self.mobs) == 0:
        	self.show_fi_screen()
        	self.quit()

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) # tirar quando acabar
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
     
        for sprite in self.all_sprites:
            if isinstance(sprite, Monstro):
                sprite.draw_health()
            if isinstance(sprite, Monstro_F):
                sprite.draw_health()
            if isinstance(sprite, Monstro_F):
                sprite.draw_health()

            # para ver as hitboxes 
            self.screen.blit(sprite.image, self.camera.apply(sprite))


        # HUD functions
        draw_player_health(self.screen, 10, 40, self.player.health / self.player.vida)
        self.draw_text('Hp  {0}-{1}'.format(self.player.health,self.player.vida), self.title_font, 25, WHITE, 225, 35, align="nw")

        draw_player_mana(self.screen, 10, 70, self.player.mana / MANA)
        self.draw_text('Mp  {0}-{1}'.format(int(self.player.mana), MANA), self.title_font, 25, WHITE, 225, 65, align="nw")

        if self.player.lvl > 3:
        	draw_player_spirit(self.screen, 10, 100, self.player.spirit / SPIRIT)
        	self.draw_text('Sp  {0}-{1}'.format(int(self.player.spirit), SPIRIT), self.title_font, 25, WHITE, 225, 95, align="nw")

        draw_player_xp(self.screen, 10, 10, self.player.xp / self.player.lvlxp)
        self.draw_text('Lvl {2} {0}-{1}'.format(self.player.xp,self.player.lvlxp, self.player.lvl), self.title_font, 25, WHITE, 525, 10, align="nw")

        if self.pause:
        	self.screen.blit(self.dim, (0, 0))
        	self.draw_text("Pause", self.title_font, 200, WHITE, WIDTH/2, HEIGHT/2, align="center")


        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_p:
                    self.pause = not self.pause
                if self.pause and event.key == pg.K_DELETE:
                	self.quit()



    def show_in_screen(self):
    	self.screen.blit(self.tela_in, (0, 0))
    	pg.display.flip()
    	self.wait_for_key2()


    def show_fi_screen(self):
    	self.screen.blit(self.tela_fi, (0, 0))
    	pg.display.flip()
    	self.wait_for_key2()
    	self.playing = False

    def show_ini_screen(self):
    	self.screen.blit(self.tela_ini, (0, 0))
    	pg.display.flip()
    	self.wait_for_key2()


    def show_mt_screen(self):
    	self.screen.blit(self.tela_mt, (0, 0))
    	pg.display.flip()
    	self.wait_for_key2()


    def show_start_screen(self):
    	self.screen.blit(self.tela_df, (0, 0))
    	pg.display.flip()
    	pg.mixer.music.play(-1)
    	self.wait_for_key()

    def GO(self):
    	pg.mixer.music.load(path.join(path.join(path.dirname(__file__), 'music'), 'Game_Over.ogg'))
    	pg.mixer.music.play(-1)
    	pg.event.wait()
    	waiting = True
    	while waiting:
    		self.clock.tick(FPS)
    		for event in pg.event.get():
    			key = pg.key.get_pressed()
    			if event.type == pg.QUIT:
    				waiting = False
    				self.quit()

    			if event.type == pg.KEYDOWN:
    				if key[pg.K_SPACE]:
    					waiting = False
    					pg.mixer.music.stop()
    					pg.mixer.music.load(path.join(path.join(path.dirname(__file__), 'music'), MUSICA_PRINCIPAL))
    					pg.mixer.music.play(-1)


    def wait_for_key(self):
    	pg.event.wait()
    	waiting = True
    	while waiting:
    		self.clock.tick(FPS)
    		for event in pg.event.get():
    			if event.type == pg.QUIT:
    				waiting = False
    				self.quit()

    			elif event.type == pg.KEYUP:
    				waiting = False
    				contagem = 1
    				if contagem == 1:
	    				pg.mixer.music.stop()
	    				pg.mixer.music.load(path.join(path.join(path.dirname(__file__), 'music'), MUSICA_PRINCIPAL))
	    				pg.mixer.music.play(-1)

    def wait_for_key2(self):
    	pg.event.wait()
    	waiting = True
    	while waiting:
    		self.clock.tick(FPS)
    		for event in pg.event.get():
    			if event.type == pg.QUIT:
    				waiting = False
    				self.quit()

    			elif event.type == pg.KEYUP:
    				waiting = False

    def show_go_screen(self):
    	self.screen.blit(self.tela_go, (0, 0))
    	pg.display.flip()
    	pg.mixer.music.stop()
    	self.GO()

# create the game tile_object
g = Game()
g.show_mt_screen()
g.show_start_screen()
g.show_in_screen()
g.show_ini_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
    g.show_in_screen()
    
 