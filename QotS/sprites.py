# Sprites e colisões
import pygame as pg
from config import *
from Mapa_Camera import collide_hit_rect
from os import path
import math
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.Spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.Spritesheet, (0, 0), (x, y, width, height))
        return image

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.andando = False
        self.subindo = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(372, 14, 34, 58)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_BOX
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_shot = 0
        self.vida = VIDA
        self.health = self.vida
        self.mana = MANA
        self.mana_regen = MANA_REGEN
        self.spirit = SPIRIT
        self.spirit_regen = SPIRIT_REGEN
        self.lvlxp = LVL_XP
        self.xp = 0
        self.lvl = 1
        

    def load_images(self):

        self.andando_e_frames = [self.game.spritesheet.get_image(322, 88, 30, 56), self.game.spritesheet.get_image(374, 86, 30, 58), self.game.spritesheet.get_image(426, 88, 30, 56)]
        for frame in self.andando_e_frames:
            frame.set_colorkey(WHITE)
        self.andando_d_frames = [self.game.spritesheet.get_image(322, 160, 30, 56), self.game.spritesheet.get_image(374, 158, 30, 58), self.game.spritesheet.get_image(426, 160, 30, 56)]
        for frame in self.andando_d_frames:
            frame.set_colorkey(WHITE)
        self.descendo_frames = [self.game.spritesheet.get_image(322, 16, 30, 56), self.game.spritesheet.get_image(372, 14, 34, 58), self.game.spritesheet.get_image(426, 16, 30, 56)]
        for frame in self.descendo_frames:
            frame.set_colorkey(WHITE)
        self.subindo_frames = [self.game.spritesheet.get_image(322, 232, 30, 56), self.game.spritesheet.get_image(372, 230, 34, 58), self.game.spritesheet.get_image(426, 232, 30, 56)]
        for frame in self.subindo_frames:
            frame.set_colorkey(WHITE)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pos()
        mouse_d = pg.mouse.get_pressed()
        # pg.mixer.music.load(path.join(path.join(path.dirname(__file__), 'music'), MUSICA_PRINCIPAL))

        if keys[pg.K_a]:  
            self.vel.x = -PLAYER_SPEED

        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED

        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED

        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED

        if self.vel.y != 0 and self.vel.x != 0:
            self.vel.y = self.vel.y / 2**(1/2)
            self.vel.x = self.vel.x / 2**(1/2)

        #teste lvl
        if keys[pg.K_l] and keys[pg.K_2]:
            self.lvl = 2

        if keys[pg.K_l] and keys[pg.K_3]:
            self.lvl = 3

        if keys[pg.K_l] and keys[pg.K_4]:
            self.lvl = 4 

        if keys[pg.K_l] and keys[pg.K_5]:
            self.lvl = 5 

        if keys[pg.K_l] and keys[pg.K_6]:
            self.lvl = 6

        if keys[pg.K_l] and keys[pg.K_7]:
            self.lvl = 7

        if keys[pg.K_l] and keys[pg.K_0]:
            self.lvl = 99

        if keys[pg.K_g]:
            self.health = self.vida

        #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


        if pg.mouse.get_pressed() == (1, 0, 0):
            now = pg.time.get_ticks()
            if now - self.last_shot > MAGIA_RATE:
                if self.mana - MANA_CUSTO > 0:
                    pg.mixer.Channel(0).play(pg.mixer.Sound(path.join(path.join(path.dirname(__file__), 'music'), FIREBALL)))
                    self.last_shot = now
                    angle_r = math.atan2((mouse[1] - HEIGHT/2), (mouse[0] - WIDTH/2))
                    angle = math.degrees(angle_r)
                    dir = vec(1, 0).rotate(angle)
                    Magia(self.game, self.pos, dir)
                    self.mana -= MANA_CUSTO

        if self.lvl > 2:
            if pg.mouse.get_pressed() == (0, 0, 1):
                now = pg.time.get_ticks()
                if now - self.last_shot > MAGIA_RATE:
                    if self.mana - MANA_CUSTO > 0:
                        pg.mixer.Channel(0).play(pg.mixer.Sound(path.join(path.join(path.dirname(__file__), 'music'), SLIMEBALL)))
                        self.last_shot = now
                        angle_r = math.atan2((mouse[1] - HEIGHT/2), (mouse[0] - WIDTH/2))
                        angle = math.degrees(angle_r)
                        dir = vec(1, 0).rotate(angle)
                        Magia_Ent(self.game, self.pos, dir)
                        self.mana -= MANA_CUSTO_

        if self.lvl > 3:
            if keys[pg.K_r]:
                now = pg.time.get_ticks()
                if now - self.last_shot > 500:
                    self.last_shot = now
                    if self.health < self.vida:
                        if self.spirit - SPIRIT_CUSTO  >= 0:
                            self.spirit -= SPIRIT_CUSTO
                            self.health += self.vida * 0.1
                            if self.health > self.vida:
                                self.health = self.vida

        if self.lvl > 4:
            if keys[pg.K_SPACE]:
                now = pg.time.get_ticks()
                if now - self.last_shot > MAGIA_RATE:
                    if self.health - CUSTO_BOLADO > self.vida * 0.25:
                        pg.mixer.Channel(0).play(pg.mixer.Sound(path.join(path.join(path.dirname(__file__), 'music'), WATERBALL)))
                        self.last_shot = now
                        angle_r = math.atan2((mouse[1] - HEIGHT/2), (mouse[0] - WIDTH/2))
                        angle = math.degrees(angle_r)
                        dir = vec(1, 0).rotate(angle)
                        Magia_Bolada(self.game, self.pos, dir)
                        self.health -= CUSTO_BOLADO

    def update(self):
        self.animate()
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.spirit > SPIRIT:
            self.spirit = SPIRIT



        self.mana_regen = 0.8 / (self.lvl ** (-0.5))
        self.vida = 400 + self.lvl * 200
        self.lvlxp = 2 ** self.lvl * 50

        if self.lvl == 4:
            self.spirit_regen = 0.02

        if self.mana + self.mana_regen <= MANA:
            self.mana += self.mana_regen
            if self.mana > MANA - 2:
                self.mana = MANA

        if self.lvl > 3:
            if self.spirit + self.spirit_regen <= SPIRIT:
                self.spirit += self.spirit_regen
                if self.spirit > SPIRIT - 2:
                    self.spirit = SPIRIT                


        if self.xp >= self.lvlxp:
            self.lvl += 1 
            self.xp = 0
            


    def animate(self):
        now = pg.time.get_ticks()
        if not self.andando and not self.subindo:
            self.image = self.descendo_frames[1]

        if self.vel.x != 0:
            self.andando = True
        else:
            self.andando = False

        if self.andando:
            if now - self.last_update >  150:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.andando_e_frames))

                if self.vel.x < 0:
                    self.image = self.andando_e_frames[self.current_frame]

                if self.vel.x > 0:
                    self.image = self.andando_d_frames[self.current_frame]

        if self.vel.y != 0:
            self.subindo = True
        else:
            self.subindo = False

        if self.subindo:
            if now - self.last_update >  150:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.subindo_frames))

                if self.vel.y < 0:
                    self.image = self.subindo_frames[self.current_frame]

                if self.vel.y > 0:
                    self.image = self.descendo_frames[self.current_frame]

class Monstro(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.andando = False
        self.subindo = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet_boar.get_image(22, 212, 68, 52)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        
        self.hit_rect = MONSTRO_HIT_BOX.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MONSTRO_HEALTH
        self.type = 1

    def load_images(self):
        self.andando_e_frames = [self.game.spritesheet_boar.get_image(22, 212, 68, 52), self.game.spritesheet_boar.get_image(152, 210, 68, 54), self.game.spritesheet_boar.get_image(282, 212, 70, 52)]
        for frame in self.andando_e_frames:
            frame.set_colorkey(WHITE)
        self.andando_d_frames = [self.game.spritesheet_boar.get_image(26, 344, 70, 52), self.game.spritesheet_boar.get_image(158, 342, 68, 54), self.game.spritesheet_boar.get_image(288, 344, 68, 52)]
        for frame in self.andando_d_frames:
            frame.set_colorkey(WHITE)
        self.descendo_frames = [self.game.spritesheet_boar.get_image(40, 74, 36, 58), self.game.spritesheet_boar.get_image(170, 72, 37, 60), self.game.spritesheet_boar.get_image(300, 74, 36, 58)]
        for frame in self.descendo_frames:
            frame.set_colorkey(WHITE)
        self.subindo_frames = [self.game.spritesheet_boar.get_image(40, 470, 36, 58), self.game.spritesheet_boar.get_image(170, 468, 36, 60), self.game.spritesheet_boar.get_image(300, 470, 36, 58)]
        for frame in self.subindo_frames:
            frame.set_colorkey(WHITE)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.game.player.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            self.animate()
            self.draw_health()
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(MONSTRO_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.player.xp += MONSTRO_XP
            self.kill()

    def draw_health(self):
        if self.health > MONSTRO_HEALTH * 0.7:
            col = DARKGREEN
        elif self.health > MONSTRO_HEALTH * 0.4:
            col = DARKYELLOW
        else:
            col = DARKRED


        #width_ = float(self.rect.width * self.health / MONSTRO_HEALTH)
        self.health_bar = pg.Rect(0, 0, MONSTRO_HIT_BOX[2], 5)

        if self.health < MONSTRO_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.andando and not self.subindo:
            self.image = self.descendo_frames[0]

        if self.vel.x != 0:
            self.andando = True
        else:
            self.andando = False

        if self.andando:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.andando_e_frames))

                if self.vel.x < 0:
                    self.image = self.andando_e_frames[self.current_frame]

                elif self.vel.x > 0:
                    self.image = self.andando_d_frames[self.current_frame]

        if self.vel.y != 0:
            self.subindo = True
        else:
            self.subindo = False

        if self.subindo:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.subindo_frames))

                if self.vel.y < 0:
                    self.image = self.subindo_frames[self.current_frame]

                if self.vel.y > 0:
                    self.image = self.descendo_frames[self.current_frame]

class Monstro_F(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.andando = False
        self.subindo = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet_element.get_image(1238, 52, 46, 76)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        
        self.hit_rect = MONSTRO_F_HIT_BOX.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MONSTRO_F_HEALTH
        self.last_shot = 0
        self.type = 2

    def load_images(self):
        self.andando_e_frames = [self.game.spritesheet_element.get_image(1120, 182, 44, 74), self.game.spritesheet_element.get_image(1240, 180, 42, 76), self.game.spritesheet_element.get_image(1360, 182, 42, 74)]
        for frame in self.andando_e_frames:
            frame.set_colorkey(WHITE)
        self.andando_d_frames = [self.game.spritesheet_element.get_image(1120, 310, 42, 74), self.game.spritesheet_element.get_image(1240, 308, 42, 77), self.game.spritesheet_element.get_image(1358, 310, 44, 74)]
        for frame in self.andando_d_frames:
            frame.set_colorkey(WHITE)
        self.descendo_frames = [self.game.spritesheet_element.get_image(1120, 54, 42, 74), self.game.spritesheet_element.get_image(1239, 54, 42, 74), self.game.spritesheet_element.get_image(1360, 54, 42, 74)]
        for frame in self.descendo_frames:
            frame.set_colorkey(WHITE)
        self.subindo_frames = [self.game.spritesheet_element.get_image(1120, 438, 42, 75), self.game.spritesheet_element.get_image(1238, 436, 46, 76), self.game.spritesheet_element.get_image(1360, 438, 42, 74)]
        for frame in self.subindo_frames:
            frame.set_colorkey(WHITE)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.game.player.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            self.animate()
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(MONSTRO_F_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.game.player.xp += MONSTRO_F_XP
            self.kill()

    def draw_health(self):
        if self.health > MONSTRO_F_HEALTH * 0.7:
            col = DARKGREEN
        elif self.health > MONSTRO_F_HEALTH * 0.4:
            col = DARKYELLOW
        else:
            col = DARKRED

        self.health_bar = pg.Rect(0, 0, MONSTRO_F_HIT_BOX[2], 5)
        if self.health < MONSTRO_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.andando and not self.subindo:
            self.image = self.descendo_frames[0]

        if self.vel.x != 0:
            self.andando = True
        else:
            self.andando = False

        if self.andando:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.andando_e_frames))

                if self.vel.x < 0:
                    self.image = self.andando_e_frames[self.current_frame]

                elif self.vel.x > 0:
                    self.image = self.andando_d_frames[self.current_frame]

        if self.vel.y != 0:
            self.subindo = True
        else:
            self.subindo = False

        if self.subindo:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.subindo_frames))

                if self.vel.y < 0:
                    self.image = self.subindo_frames[self.current_frame]

                if self.vel.y > 0:
                    self.image = self.descendo_frames[self.current_frame]

class Monstro_A(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.andando = False
        self.subindo = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet_element.get_image(30, 66, 62, 62)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        
        self.hit_rect = MONSTRO_A_HIT_BOX.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MONSTRO_A_HEALTH
        self.last_shot = 0
        self.type = 3
        self.last_shot = 0

    def load_images(self):
        self.andando_e_frames = [self.game.spritesheet_element.get_image(38, 194, 46, 62), self.game.spritesheet_element.get_image(158, 192, 46, 64), self.game.spritesheet_element.get_image(278, 194, 44, 62)]
        for frame in self.andando_e_frames:
            frame.set_colorkey(WHITE)
        self.andando_d_frames = [self.game.spritesheet_element.get_image(36, 322, 45, 62), self.game.spritesheet_element.get_image(154, 320, 46, 64), self.game.spritesheet_element.get_image(274, 322, 46, 62)]
        for frame in self.andando_d_frames:
            frame.set_colorkey(WHITE)
        self.descendo_frames = [self.game.spritesheet_element.get_image(30, 66, 62, 62), self.game.spritesheet_element.get_image(148, 64, 62, 64), self.game.spritesheet_element.get_image(266, 66, 62, 62)]
        for frame in self.descendo_frames:
            frame.set_colorkey(WHITE)
        self.subindo_frames = [self.game.spritesheet_element.get_image(26, 450, 62, 62), self.game.spritesheet_element.get_image(148, 448, 62, 64), self.game.spritesheet_element.get_image(270, 450, 62, 62)]
        for frame in self.subindo_frames:
            frame.set_colorkey(WHITE)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.game.player.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            self.animate()
            self.draw_health()
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(-MONSTRO_A_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            angle_r = math.atan2((self.game.player.pos.y - self.pos.y), (self.game.player.pos.x - self.pos.x))
            angle = math.degrees(angle_r)
            dir = vec(1, 0).rotate(angle)
            now = pg.time.get_ticks()
            if now - self.last_shot > 1000:
                self.last_shot = now
                Magia_A(self.game, self.pos, dir) 

        if self.health <= 0:
            self.game.player.xp += MONSTRO_A_XP
            self.game.player.spirit += 5
            self.kill()

    def draw_health(self):
        if self.health > MONSTRO_A_HEALTH * 0.7:
            col = DARKGREEN
        elif self.health > MONSTRO_A_HEALTH * 0.4:
            col = DARKYELLOW
        else:
            col = DARKRED

        self.health_bar = pg.Rect(0, 0, MONSTRO_A_HIT_BOX[2], 5)
        if self.health < MONSTRO_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.andando and not self.subindo:
            self.image = self.descendo_frames[0]

        if self.vel.x != 0:
            self.andando = True
        else:
            self.andando = False

        if self.andando:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.andando_e_frames))

                if self.vel.x < 0:
                    self.image = self.andando_e_frames[self.current_frame]

                elif self.vel.x > 0:
                    self.image = self.andando_d_frames[self.current_frame]

        if self.vel.y != 0:
            self.subindo = True
        else:
            self.subindo = False

        if self.subindo:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.subindo_frames))

                if self.vel.y < 0:
                    self.image = self.subindo_frames[self.current_frame]

                if self.vel.y > 0:
                    self.image = self.descendo_frames[self.current_frame]

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.andando = False
        self.subindo = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet_boss.get_image(526, 10, 38, 62)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        
        self.hit_rect = BOSS_HIT_BOX.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = BOSS_HEALTH
        self.last_shot = 0
        self.type = 3
        self.last_shot = 0

    def load_images(self):

        self.andando_e_frames = [self.game.spritesheet_boss.get_image(474, 84, 38, 60), self.game.spritesheet_boss.get_image(530, 82, 29, 62), self.game.spritesheet_boss.get_image(582, 84, 30, 62)]
        for frame in self.andando_e_frames:
            frame.set_colorkey(WHITE)
        self.andando_d_frames = [self.game.spritesheet_boss.get_image(478, 156, 30, 60), self.game.spritesheet_boss.get_image(530, 154, 30, 62), self.game.spritesheet_boss.get_image(578, 156, 38, 60)]
        for frame in self.andando_d_frames:
            frame.set_colorkey(WHITE)
        self.descendo_frames = [self.game.spritesheet_boss.get_image(476, 12, 32, 60), self.game.spritesheet_boss.get_image(526, 10, 38, 62), self.game.spritesheet_boss.get_image(582, 12, 32, 60)]
        for frame in self.descendo_frames:
            frame.set_colorkey(WHITE)
        self.subindo_frames = [self.game.spritesheet_boss.get_image(476, 228, 32, 60), self.game.spritesheet_boss.get_image(526, 226, 38, 62), self.game.spritesheet_boss.get_image(582, 228, 32, 60)]
        for frame in self.subindo_frames:
            frame.set_colorkey(WHITE)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.game.player.pos - self.pos
        if target_dist.length_squared() < (DETECT_RADIUS - 70)**2:
            self.animate()
            self.draw_health()
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(BOSS_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            angle_r = math.atan2((self.game.player.pos.y - self.pos.y), (self.game.player.pos.x - self.pos.x))
            angle = math.degrees(angle_r)
            dir = vec(1, 0).rotate(angle)
            now = pg.time.get_ticks()
            if now - self.last_shot > 1000:
                self.last_shot = now
                Magia_B(self.game, self.pos, dir) 

        if self.health <= 0:
            self.game.player.xp += BOSS_XP
            self.kill()
            self.game.show_fi_screen()
            pg.time.wait(3000)


    def draw_health(self):
        if self.health > BOSS_HEALTH * 0.7:
            col = DARKGREEN
        elif self.health > BOSS_HEALTH * 0.4:
            col = DARKYELLOW
        else:
            col = DARKRED

        self.health_bar = pg.Rect(0, 0, BOSS_HIT_BOX[2], 5)
        if self.health < BOSS_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.andando and not self.subindo:
            self.image = self.descendo_frames[0]

        if self.vel.x != 0:
            self.andando = True
        else:
            self.andando = False

        if self.andando:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.andando_e_frames))

                if self.vel.x < 0:
                    self.image = self.andando_e_frames[self.current_frame]

                elif self.vel.x > 0:
                    self.image = self.andando_d_frames[self.current_frame]

        if self.vel.y != 0:
            self.subindo = True
        else:
            self.subindo = False

        if self.subindo:
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = ((self.current_frame +1) % len(self.subindo_frames))

                if self.vel.y < 0:
                    self.image = self.subindo_frames[self.current_frame]

                if self.vel.y > 0:
                    self.image = self.descendo_frames[self.current_frame]

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Vida(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.vida
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect

class Magia(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.magias_p
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.magia_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * MAGIA_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MAGIA_LIFETIME:
            self.kill()

class Magia_Bolada(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.magias_b
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.magia_bolada_img 
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * MAGIA_SPEED * 0.5
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MAGIA_LIFETIME + 500:
            self.kill()

class Magia_Ent(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.magias_m
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.magia_f_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * MAGIA_SPEED * 0.6
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MAGIA_LIFETIME:
            self.kill()

class Magia_A(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.magias_a
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.spritesheet_element.get_image(159, 590, 39, 50),(20, 25))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * MAGIA_SPEED * 0.2
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > 5000:
            self.kill()

class Magia_B(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.magias_a
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.magia_b,(20, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * MAGIA_SPEED * 0.7
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > 1700:
            self.kill()