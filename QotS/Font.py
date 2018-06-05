# Código fonte
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
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
           #pg.key.set_repeat(500, 100)
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'imagens')
        map_folder = path.join(game_folder, 'map')
        self.map = TiledMap(path.join(map_folder, 'mapao.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, BONECO)).convert_alpha()
        self.magia_img = pg.image.load(path.join(img_folder, MAGIA_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MONSTRO_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.wall_grass_img = pg.image.load(path.join(img_folder, WALL_GRASS_IMG)).convert_alpha()
        self.wall_grass_img = pg.transform.scale(self.wall_grass_img, (TILESIZE, TILESIZE))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.magias = pg.sprite.Group()
        self.atks = pg.sprite.Group()


        for tile_object in self.map.tmxdata.objects:
        	if tile_object.name == 'player spawn':
        		self.player = Player(self, tile_object.x, tile_object.y)
        	if tile_object.name == 'mob spawn':
        		Monstro(self, tile_object.x, tile_object.y)
        	if tile_object.name == 'parede':
        		Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.ver = False

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        hits_m = pg.sprite.groupcollide(self.mobs, self.magias, False, True)
        for hit in hits_m:
        	hit.health -= ATK_DMG

        for hit in hits:
            self.player.health -= DANO_MONSTRO
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False

        if hits:
            self.player.pos += vec(MONTRO_PUSH, 0). rotate(-hits[0].rot)

    def draw(self):
        #pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) # tirar quando acabar
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
     
        for sprite in self.all_sprites:
            if isinstance(sprite, Monstro):
                sprite.draw_health()
            # para ver as hitboxes
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.ver:
            	pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.ver:
        	for wall in self.walls:
        		pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)

        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / VIDA)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_x:
                	self.ver = not self.ver

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
